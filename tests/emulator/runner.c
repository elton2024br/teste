/* Headless mGBA test driver. Ordinary saves are backed by --save, never states. */
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint32_t save_block_ptr_symbol, party_count_symbol;
static void logmsg(struct mLogger *logger, int category, enum mLogLevel level,
                   const char *format, va_list args)
{
    (void)logger;
    if (level == mLOG_FATAL || level == mLOG_ERROR) {
        fprintf(stderr, "%s: ", mLogCategoryName(category));
        vfprintf(stderr, format, args);
        fputc('\n', stderr);
    }
}

static int load_symbols(const char *path)
{
    FILE *file = fopen(path, "r");
    if (!file) return 0;
    char line[512], type, name[256];
    unsigned address;
    while (fgets(line, sizeof(line), file)) {
        if (sscanf(line, "%x %c %255s", &address, &type, name) != 3) continue;
        if (!strcmp(name, "gSaveBlock1Ptr")) save_block_ptr_symbol = address;
        if (!strcmp(name, "gPlayerPartyCount")) party_count_symbol = address;
    }
    fclose(file);
    return save_block_ptr_symbol && party_count_symbol;
}

int main(int argc, char **argv)
{
    const char *save_path = NULL, *symbols_path = NULL;
    if (argc < 2) return 2;
    for (int i = 2; i < argc; i += 2) {
        if (i + 1 >= argc) return 2;
        if (!strcmp(argv[i], "--save")) save_path = argv[i + 1];
        else if (!strcmp(argv[i], "--symbols")) symbols_path = argv[i + 1];
        else return 2;
    }
    if (symbols_path && !load_symbols(symbols_path)) {
        fprintf(stderr, "Missing required symbols in %s\n", symbols_path);
        return 2;
    }
    struct mLogger logger = {.log = logmsg, .filter = NULL};
    mLogSetDefaultLogger(&logger);
    struct mCore *core = mCoreFind(argv[1]);
    if (!core || !core->init(core)) return 3;
    mCoreInitConfig(core, NULL);
    int result = 0;
    color_t *pixels = NULL;
    if (!mCoreLoadFile(core, argv[1])) { result = 4; goto cleanup; }
    pixels = calloc(240 * 160, sizeof(*pixels));
    if (!pixels) { result = 5; goto cleanup; }
    core->setVideoBuffer(core, pixels, 240);
    if (save_path) {
        struct VFile *file = VFileOpen(save_path, O_RDWR | O_CREAT);
        if (!file) { result = 9; goto cleanup; }
        if (!core->loadSave(core, file)) {
            file->close(file);
            result = 9;
            goto cleanup;
        }
        /* The core owns the VFile and persists its native save backing. */
    }
    core->reset(core);
    char line[1024];
    unsigned keys, frames, address;
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (sscanf(line, "run %u %u", &keys, &frames) == 2) {
            core->setKeys(core, keys);
            for (unsigned i = 0; i < frames; i++) core->runFrame(core);
            printf("FRAME %u\n", core->frameCounter(core));
        } else if (!strncmp(line, "shot ", 5)) {
            FILE *file = fopen(line + 5, "wb");
            if (!file) { result = 5; break; }
            fprintf(file, "P6\n240 160\n255\n");
            for (int i = 0; i < 240 * 160; i++) {
                uint32_t pixel = pixels[i];
                fputc(pixel & 255, file);
                fputc((pixel >> 8) & 255, file);
                fputc((pixel >> 16) & 255, file);
            }
            int failed = ferror(file);
            if (fclose(file)) failed = 1;
            if (failed) { result = 5; break; }
            puts("SHOT");
        } else if (!strncmp(line, "save ", 5) || !strncmp(line, "load ", 5)) {
            int writing = line[0] == 's';
            size_t size = core->stateSize(core);
            void *data = malloc(size);
            if (!data) { result = 6; break; }
            FILE *file = fopen(line + 5, writing ? "wb" : "rb");
            int ok = file != NULL;
            if (ok && writing) ok = core->saveState(core, data) && fwrite(data, 1, size, file) == size;
            if (ok && !writing) ok = fread(data, 1, size, file) == size && core->loadState(core, data);
            if (file && fclose(file)) ok = 0;
            free(data);
            if (!ok) { result = writing ? 6 : 7; break; }
            puts(writing ? "STATE_SAVED" : "STATE_LOADED");
        } else if (sscanf(line, "read32 %x", &address) == 1) {
            printf("READ32 %08X %08X\n", address, core->busRead32(core, address));
        } else if (sscanf(line, "read8 %x", &address) == 1) {
            printf("READ8 %08X %02X\n", address, core->busRead8(core, address));
        } else if (!strcmp(line, "progress")) {
            if (!save_block_ptr_symbol || !party_count_symbol) {
                fprintf(stderr, "progress requires --symbols from this build's arm-none-eabi-nm output\n");
                result = 14;
                break;
            }
            uint32_t block = core->busRead32(core, save_block_ptr_symbol);
            if (block < 0x02000000 || block > 0x0203E000) {
                puts("PROGRESS unavailable");
            } else {
                /* SaveBlock1 offsets belong to the pinned FireRed source. */
                printf("PROGRESS base=%08X partner=%u flags=%02X keyitem=%u party=%u starter=%u map=%u/%u\n",
                    block, !!(core->busRead8(core, block + 0xF74) & 0x80),
                    core->busRead8(core, block + 0xF75), core->busRead16(core, block + 0x3B8),
                    core->busRead8(core, party_count_symbol), core->busRead16(core, block + 0x1062),
                    core->busRead8(core, block + 4), core->busRead8(core, block + 5));
            }
        } else if (!strcmp(line, "flushsave")) {
            /* No cloning/truncating a live native save file. Close the core instead. */
            fprintf(stderr, "flushsave removed: save through the game menu, then quit normally\n");
            result = 15;
            break;
        } else if (!strcmp(line, "quit")) break;
        else if (*line) { fprintf(stderr, "Unknown command: %s\n", line); result = 2; break; }
        fflush(stdout);
    }
cleanup:
    core->deinit(core);
    free(pixels);
    return result;
}
