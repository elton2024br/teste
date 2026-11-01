#include <mgba/core/core.h>
#include <stdio.h>
#include <mgba/core/log.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <mgba-util/vfs.h>
#include <fcntl.h>
static void logmsg(struct mLogger*l,int cat,enum mLogLevel level,const char*fmt,va_list args){if(level==mLOG_FATAL||level==mLOG_ERROR){fprintf(stderr,"%s: ",mLogCategoryName(cat));vfprintf(stderr,fmt,args);fputc(10,stderr);}}
int main(int argc,char**argv){
 struct mLogger logger={.log=logmsg,.filter=NULL};mLogSetDefaultLogger(&logger);
 if(argc!=2 && !(argc==4 && !strcmp(argv[2],"--save")))return 2;
 struct mCore*c=mCoreFind(argv[1]); if(!c||!c->init(c))return 3;
 mCoreInitConfig(c,NULL); if(!mCoreLoadFile(c,argv[1]))return 4;
 color_t* pixels=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,pixels,240);
 if(argc==4){struct VFile*vf=VFileOpen(argv[3],O_RDWR|O_CREAT);if(!vf||!c->loadSave(c,vf))return 9;}
 c->reset(c);
 char cmd[512];unsigned keys,frames;
 while(fgets(cmd,sizeof(cmd),stdin)){
 if(sscanf(cmd,"run %u %u",&keys,&frames)==2){c->setKeys(c,keys);for(unsigned i=0;i<frames;i++)c->runFrame(c);printf("FRAME %u\n",c->frameCounter(c));}
 else if(!strncmp(cmd,"shot ",5)){char path[450];sscanf(cmd+5,"%449s",path);FILE*f=fopen(path,"wb");if(!f)return 5;fprintf(f,"P6\n240 160\n255\n");for(int i=0;i<240*160;i++){uint32_t p=pixels[i];fputc(p&255,f);fputc((p>>8)&255,f);fputc((p>>16)&255,f);}fclose(f);puts("SHOT");}
 else if(!strncmp(cmd,"save ",5)){char path[450];sscanf(cmd+5,"%449s",path);size_t n=c->stateSize(c);void*b=malloc(n);if(!c->saveState(c,b))return 6;FILE*f=fopen(path,"wb");fwrite(b,1,n,f);fclose(f);free(b);puts("SAVED");}
 else if(!strncmp(cmd,"load ",5)){char path[450];sscanf(cmd+5,"%449s",path);size_t n=c->stateSize(c);void*b=malloc(n);FILE*f=fopen(path,"rb");if(!f||fread(b,1,n,f)!=n)return 7;fclose(f);if(!c->loadState(c,b))return 8;free(b);puts("LOADED");}
 else if(!strncmp(cmd,"read32 ",7)){unsigned a;sscanf(cmd+7,"%x",&a);printf("READ32 %08X %08X\n",a,c->busRead32(c,a));}
 else if(!strncmp(cmd,"read8 ",6)){unsigned a;sscanf(cmd+6,"%x",&a);printf("READ8 %08X %02X\n",a,c->busRead8(c,a));}
 else if(!strncmp(cmd,"flushsave",9)){if(argc!=4)return 10;void*data=NULL;size_t n=c->savedataClone(c,&data);if(!n||!data)return 11;FILE*f=fopen(argv[3],"wb");if(!f)return 12;if(fwrite(data,1,n,f)!=n)return 13;fclose(f);free(data);printf("SAVEFILE %zu\n",n);}
 else if(!strncmp(cmd,"progress",8)){uint32_t b=c->busRead32(c,0x03005008);printf("PROGRESS base=%08X flags=%02X keyitem=%u party=%u\n",b,c->busRead8(c,b+0xF75),c->busRead16(c,b+0x3B8),c->busRead8(c,0x02024029));}
 else if(!strncmp(cmd,"quit",4))break;
 fflush(stdout);
 }c->deinit(c);free(pixels);return 0;
}
