.equ SIGN_LADY_READY, VAR_TEMP_2

PalletTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PalletTown_AmazonTransition
	.byte 0

PalletTown_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_PALLET_TOWN
	call_if_set FLAG_PALLET_LADY_NOT_BLOCKING_SIGN, PalletTown_EventScript_TryReadySignLady
	call_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 0, PalletTown_EventScript_SetSignLadyPos
	call_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1, PalletTown_EventScript_SetSignLadyDone
	end

PalletTown_EventScript_TryReadySignLady::
	goto_if_unset FLAG_OPENED_START_MENU, EventScript_Return
	goto_if_ge VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1, EventScript_Return
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1
	return

PalletTown_EventScript_SetSignLadyDone::
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 2
	return

PalletTown_EventScript_SetSignLadyPos::
	goto_if_set FLAG_PALLET_LADY_NOT_BLOCKING_SIGN, PalletTown_EventScript_MoveSignLadyToRouteEntrance
	setobjectxyperm LOCALID_PALLET_SIGN_LADY, 5, 15
	setobjectmovementtype LOCALID_PALLET_SIGN_LADY, MOVEMENT_TYPE_FACE_UP
	return

PalletTown_EventScript_MoveSignLadyToRouteEntrance::
	setobjectxyperm LOCALID_PALLET_SIGN_LADY, 12, 2
	setobjectmovementtype LOCALID_PALLET_SIGN_LADY, MOVEMENT_TYPE_FACE_DOWN
	setvar SIGN_LADY_READY, TRUE
	return

PalletTown_OnFrame::
	map_script_2 VAR_MAP_SCENE_PALLET_TOWN_OAK, 2, PalletTown_EventScript_OakRatingScene
	.2byte 0

@ Oak approaches player after exiting their house post Elite Four to check if they should receieve the National Dex
PalletTown_EventScript_OakRatingScene::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	setobjectxyperm LOCALID_PALLET_PROF_OAK, 14, 14
	setobjectmovementtype LOCALID_PALLET_PROF_OAK, MOVEMENT_TYPE_FACE_LEFT
	addobject LOCALID_PALLET_PROF_OAK
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakWalkToPlayersDoor
	waitmovement 0
	goto_if_unset FLAG_WORLD_MAP_ONE_ISLAND, PalletTown_EventScript_NotBeenToOneIslandYet
	msgbox PalletTown_Text_OakLetMeSeePokedex
	setvar VAR_0x8004, 0
	specialvar VAR_RESULT, GetPokedexCount
	copyvar VAR_0x8008, VAR_0x8005
	copyvar VAR_0x8009, VAR_0x8006
	buffernumberstring STR_VAR_1, VAR_0x8008
	buffernumberstring STR_VAR_2, VAR_0x8009
	goto_if_lt VAR_0x8009, 60, PalletTown_EventScript_NotEnoughMonsForNationalDex
	msgbox PalletTown_Text_CaughtXImpressiveFollowMe
	closemessage
	playbgm MUS_FOLLOW_ME, 0
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerWalkToLabFromHouse
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakWalkToLabFromHouse
	waitmovement 0
	opendoor 16, 13
	waitdooranim
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakEnterLab
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerEnterLab
	waitmovement 0
	closedoor 16, 13
	waitdooranim
	setvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 7
	setvar VAR_MAP_SCENE_PALLET_TOWN_OAK, 3
	setflag FLAG_HIDE_OAK_IN_PALLET_TOWN
	warp MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB, 6, 12
	waitstate
	releaseall
	end

PalletTown_EventScript_EndOakRatingScene::
	closemessage
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakExit
	waitmovement 0
	removeobject LOCALID_PALLET_PROF_OAK
	setvar VAR_MAP_SCENE_PALLET_TOWN_OAK, 3
	releaseall
	end

PalletTown_EventScript_NotEnoughMonsForNationalDex::
	msgbox PalletTown_Text_CaughtXPuttingInHonestEffort
	goto PalletTown_EventScript_EndOakRatingScene
	end

PalletTown_EventScript_NotBeenToOneIslandYet::
	msgbox PalletTown_Text_OakYouEnjoyingTraveling
	goto PalletTown_EventScript_EndOakRatingScene
	end

PalletTown_Movement_OakWalkToPlayersDoor::
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_up
	step_end

PalletTown_Movement_OakExit::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_Movement_OakWalkToLabFromHouse::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_up
	step_end

PalletTown_Movement_PlayerWalkToLabFromHouse::
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

PalletTown_EventScript_OakTriggerLeft::
	lockall
	setvar VAR_TEMP_1, 0
	goto PalletTown_EventScript_OakTrigger
	end

PalletTown_EventScript_OakTriggerRight::
	lockall
	setvar VAR_TEMP_1, 1
	goto PalletTown_EventScript_OakTrigger
	end

PalletTown_EventScript_OakTrigger::
	famechecker FAMECHECKER_OAK, FCPICKSTATE_COLORED, UpdatePickStateFromSpecialVar8005
	textcolor NPC_TEXT_COLOR_MALE
	delay 30
	playbgm MUS_OAK, 0
	message PalletTown_Text_OakDontGoOut
	waitmessage
	delay 85
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	delay 30
	addobject LOCALID_PALLET_PROF_OAK
	call_if_eq VAR_TEMP_1, 0, PalletTown_EventScript_OakEnterLeft
	call_if_eq VAR_TEMP_1, 1, PalletTown_EventScript_OakEnterRight
	delay 30
	msgbox PalletTown_Text_OakGrassUnsafeNeedMon
	closemessage
	delay 30
	call_if_eq VAR_TEMP_1, 0, PalletTown_EventScript_OakLeadPlayerToLabLeft
	call_if_eq VAR_TEMP_1, 1, PalletTown_EventScript_OakLeadPlayerToLabRight
	opendoor 16, 13
	waitdooranim
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakEnterLab
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerEnterLab
	waitmovement 0
	closedoor 16, 13
	waitdooranim
	setvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 1
	clearflag FLAG_HIDE_OAK_IN_HIS_LAB
	setvar VAR_MAP_SCENE_PALLET_TOWN_OAK, 1
	setflag FLAG_HIDE_OAK_IN_PALLET_TOWN
	setflag FLAG_DONT_TRANSITION_MUSIC
	warp MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB, 6, 12
	waitstate
	releaseall
	end

PalletTown_EventScript_OakEnterLeft::
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakEnterLeft
	waitmovement 0
	return

PalletTown_EventScript_OakEnterRight::
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakEnterRight
	waitmovement 0
	return

PalletTown_EventScript_OakLeadPlayerToLabLeft::
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakWalkToLabLeft
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerWalkToLabLeft
	waitmovement 0
	return

PalletTown_EventScript_OakLeadPlayerToLabRight::
	applymovement LOCALID_PALLET_PROF_OAK, PalletTown_Movement_OakWalkToLabRight
	applymovement LOCALID_PLAYER, PalletTown_Movement_PlayerWalkToLabRight
	waitmovement 0
	return

PalletTown_Movement_OakEnterLeft::
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	step_end

PalletTown_Movement_OakEnterRight::
	walk_right
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	step_end

	.macro walk_to_lab
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	.endm

PalletTown_Movement_OakWalkToLabLeft::
	walk_down
	walk_to_lab
	walk_right
	walk_in_place_faster_up
	step_end

PalletTown_Movement_OakWalkToLabRight::
	walk_down
	walk_left
	walk_to_lab
	walk_right
	walk_in_place_faster_up
	step_end

PalletTown_Movement_OakEnterLab::
	walk_up
	set_invisible
	step_end

PalletTown_Movement_PlayerWalkToLabLeft::
	walk_down
	walk_down
	walk_to_lab
	step_end

PalletTown_Movement_PlayerWalkToLabRight::
	walk_down
	walk_down
	walk_left
	walk_to_lab
	step_end

PalletTown_Movement_PlayerEnterLab::
	walk_right
	walk_up
	set_invisible
	step_end

PalletTown_EventScript_SignLady::
	lock
	goto_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 2, PalletTown_EventScript_SignLadyDone
	goto_if_eq VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1, PalletTown_EventScript_SignLadyJustShowedSign
	goto_if_eq SIGN_LADY_READY, TRUE, PalletTown_EventScript_SignLadyStartShowSign
	goto_if_set FLAG_TEMP_2, PalletTown_EventScript_SignLadyGoReadSign
	msgbox PalletTown_Text_HmmIsThatRight
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_Delay48
	waitmovement 0
	msgbox PalletTown_Text_OhLookLook
	closemessage
	call_if_eq VAR_FACING, DIR_EAST, PalletTown_EventScript_SignLadyMoveOutOfWayRight
	call_if_ne VAR_FACING, DIR_EAST, PalletTown_EventScript_SignLadyMoveOutOfWayLeft
	copyobjectxytoperm LOCALID_PALLET_SIGN_LADY
	setflag FLAG_TEMP_2
	release
	end

PalletTown_EventScript_SignLadyMoveOutOfWayRight::
	applymovement LOCALID_PALLET_SIGN_LADY, PalletTown_Movement_SignLadyMoveOutOfWayRight
	waitmovement 0
	return

PalletTown_EventScript_SignLadyMoveOutOfWayLeft::
	applymovement LOCALID_PALLET_SIGN_LADY, PalletTown_Movement_SignLadyMoveOutOfWayLeft
	waitmovement 0
	return

PalletTown_EventScript_SignLadyDone::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox PalletTown_Text_RaisingMonsToo
	release
	end

PalletTown_EventScript_SignLadyGoReadSign::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox PalletTown_Text_ReadItReadIt
	release
	end

PalletTown_EventScript_SignLadyJustShowedSign::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox PalletTown_Text_SignsAreUsefulArentThey
	release
	end

PalletTown_Movement_SignLadyMoveOutOfWayRight::
	walk_right
	walk_in_place_faster_left
	step_end

PalletTown_Movement_SignLadyMoveOutOfWayLeft::
	walk_left
	walk_in_place_faster_right
	step_end

PalletTown_EventScript_FatMan::
	msgbox PalletTown_Text_CanStoreItemsAndMonsInPC, MSGBOX_NPC
	end

PalletTown_EventScript_OaksLabSign::
	lockall
	famechecker FAMECHECKER_OAK, 0
	msgbox PalletTown_Text_OakPokemonResearchLab
	releaseall
	end

PalletTown_EventScript_PlayersHouseSign::
	msgbox PalletTown_Text_PlayersHouse, MSGBOX_SIGN
	end

PalletTown_EventScript_RivalsHouseSign::
	msgbox PalletTown_Text_RivalsHouse, MSGBOX_SIGN
	end

PalletTown_EventScript_TownSign::
	msgbox PalletTown_Text_TownSign, MSGBOX_SIGN
	end

PalletTown_EventScript_TrainerTips::
	lockall
	msgbox PalletTown_Text_PressStartToOpenMenu
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1
	releaseall
	end

PalletTown_EventScript_SignLadyTrigger::
	lockall
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_WalkInPlaceFasterRight
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	call PalletTown_EventScript_SignLadyShowSign
	releaseall
	end

PalletTown_EventScript_SignLadyShowSign::
	textcolor NPC_TEXT_COLOR_FEMALE
	msgbox PalletTown_Text_LookCopiedTrainerTipsSign
	closemessage
	delay 20
	textcolor NPC_TEXT_COLOR_NEUTRAL
	setflag FLAG_OPENED_START_MENU
	setvar VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY, 1
	setvar SIGN_LADY_READY, FALSE
	special SetWalkingIntoSignVars
	special DisableMsgBoxWalkaway
	signmsg
	msgbox PalletTown_Text_PressStartToOpenMenuCopy
	normalmsg
	return

PalletTown_EventScript_SignLadyStartShowSign::
	applymovement LOCALID_PALLET_SIGN_LADY, Common_Movement_FacePlayer
	waitmovement 0
	call PalletTown_EventScript_SignLadyShowSign
	release
	end

PalletTown_AmazonTransition::
	setflag FLAG_TEMP_1
	setrespawn HEAL_LOCATION_PALLET_TOWN
	end

Amazon_EventScript_ChoosePartner::
    lock
    faceplayer
    goto_if_set FLAG_AMAZON_PARTNER_CHOSEN, Amazon_EventScript_Supplies
    msgbox Amazon_Text_Welcome, MSGBOX_DEFAULT
Amazon_EventScript_Selection::
    multichoice 0, 0, MULTICHOICE_AMAZON_STARTERS, FALSE
    goto_if_eq VAR_RESULT, 0, Amazon_EventScript_Capybara
    goto_if_eq VAR_RESULT, 1, Amazon_EventScript_Macaw
    goto_if_eq VAR_RESULT, 2, Amazon_EventScript_Armadillo
    release
    end
Amazon_EventScript_Capybara::
    setvar VAR_0x8004, SPECIES_SQUIRTLE
    setvar VAR_0x8005, 1
    showmonpic SPECIES_SQUIRTLE, 10, 3
    msgbox Amazon_Text_Capybara, MSGBOX_YESNO
    goto Amazon_EventScript_Confirm
Amazon_EventScript_Macaw::
    setvar VAR_0x8004, SPECIES_CHARMANDER
    setvar VAR_0x8005, 2
    showmonpic SPECIES_CHARMANDER, 10, 3
    msgbox Amazon_Text_Macaw, MSGBOX_YESNO
    goto Amazon_EventScript_Confirm
Amazon_EventScript_Armadillo::
    setvar VAR_0x8004, SPECIES_BULBASAUR
    setvar VAR_0x8005, 0
    showmonpic SPECIES_BULBASAUR, 10, 3
    msgbox Amazon_Text_Armadillo, MSGBOX_YESNO
Amazon_EventScript_Confirm::
    hidemonpic
    goto_if_ne VAR_RESULT, YES, Amazon_EventScript_Selection
    getpartysize
    goto_if_ne VAR_RESULT, 0, Amazon_EventScript_PartyNotEmpty
    givemon VAR_0x8004, 5
    goto_if_ne VAR_RESULT, MON_GIVEN_TO_PARTY, Amazon_EventScript_PartyNotEmpty
    copyvar VAR_STARTER_MON, VAR_0x8005
    setflag FLAG_AMAZON_PARTNER_CHOSEN
    setflag FLAG_SYS_POKEMON_GET
    msgbox Amazon_Text_PartnerReceived, MSGBOX_DEFAULT
Amazon_EventScript_Supplies::
    goto_if_set FLAG_AMAZON_SUPPLIES_RECEIVED, Amazon_EventScript_AlreadyChosen
    checkitemspace ITEM_POKE_BALL, 5
    goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_NoRoom
    additem ITEM_POKE_BALL, 5
    goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_NoRoom
    setflag FLAG_AMAZON_SUPPLIES_RECEIVED
    msgbox Amazon_Text_Supplies, MSGBOX_DEFAULT
    release
    end
Amazon_EventScript_AlreadyChosen::
    goto_if_set FLAG_AMAZON_WATER_STONE, Amazon_EventScript_Returned
    msgbox Amazon_Text_AlreadyChosen, MSGBOX_DEFAULT
    release
    end
Amazon_EventScript_NoRoom::
    msgbox Amazon_Text_NoRoom, MSGBOX_DEFAULT
    release
    end
Amazon_EventScript_PartyNotEmpty::
    msgbox Amazon_Text_GrantFailed, MSGBOX_DEFAULT
    release
    end
Amazon_Text_Welcome::
    .string "Nossa jornada começa aqui!\p"
    .string "Escolha um parceiro para\n"
    .string "explorar a floresta.$"
Amazon_Text_Capybara::
    .string "CAPIVÁGUA - ÁGUA\p"
    .string "Calma e resistente, segue\n"
    .string "o ritmo dos rios. Escolher?$"
Amazon_Text_Macaw::
    .string "ARARAFOGO - FOGO\p"
    .string "Ágil e cheia de energia.\n"
    .string "Escolher este parceiro?$"
Amazon_Text_Armadillo::
    .string "TATUPEDRA - TERRA\p"
    .string "Uma armadura para proteger\n"
    .string "seus amigos. Escolher?$"
Amazon_Text_PartnerReceived::
    .string "Você recebeu seu parceiro!$"
Amazon_Text_Supplies::
    .string "Receba cinco cápsulas\n"
    .string "para encontrar novos amigos!$"
Amazon_Text_AlreadyChosen::
    .string "A empresa bloqueou o rio!\p"
    .string "Siga ao norte e liberte a passagem.$"
Amazon_Text_NoRoom::
    .string "Abra espaço na mochila e\n"
    .string "volte para buscar as cápsulas.$"
Amazon_Text_GrantFailed::
    .string "Vamos conferir sua equipe\n"
    .string "antes de seguir.$"

Amazon_EventScript_Returned::
    msgbox Amazon_Text_Returned, MSGBOX_DEFAULT
    release
    end
Amazon_EventScript_Caregiver::
    lock
    faceplayer
    goto_if_unset FLAG_AMAZON_WATER_STONE, Amazon_EventScript_CareHeal
    checkitem ITEM_PEDRA_DAS_AGUAS
    goto_if_eq VAR_RESULT, TRUE, Amazon_EventScript_CareHeal
    checkitemspace ITEM_PEDRA_DAS_AGUAS, 1
    goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_CareFull
    additem ITEM_PEDRA_DAS_AGUAS, 1
    goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_CareFull
Amazon_EventScript_CareHeal::
    call EventScript_OutOfCenterPartyHeal
    msgbox Amazon_Text_Care, MSGBOX_DEFAULT
    release
    end
Amazon_EventScript_CareFull::
    msgbox Amazon_Text_CareFull, MSGBOX_DEFAULT
    release
    end
Amazon_Text_Returned::
    .string "O rio está livre! Você trouxe\n"
    .string "a Pedra das Águas!\p"
    .string "Faltam quatro pedras para abrir\n"
    .string "o caminho das Terras Raras.$"
Amazon_Text_Care::
    .string "Seus parceiros descansaram!\p"
    .string "Volte sempre que precisar.$"
Amazon_Text_CareFull::
    .string "Sua pedra precisa voltar à bolsa.\n"
    .string "Abra espaço e fale comigo.$"

Amazon_EventScript_NeedPartner::
    goto_if_set FLAG_AMAZON_PARTNER_CHOSEN, Amazon_EventScript_LeaveVillage
    lockall
    msgbox Amazon_Text_NeedPartner, MSGBOX_DEFAULT
    applymovement LOCALID_PLAYER, Amazon_Movement_StepBack
    waitmovement 0
    releaseall
    end
Amazon_EventScript_LeaveVillage::
    setvar VAR_TEMP_1, 1
    end
Amazon_Movement_StepBack::
    walk_down
    step_end
Amazon_Text_NeedPartner::
    .string "Escolha seu parceiro na vila\n"
    .string "antes de entrar na floresta.$"

Amazon_EventScript_VillageStorage::
    lockall
    goto_if_unset FLAG_AMAZON_PARTNER_CHOSEN, Amazon_EventScript_StorageNeedsPartner
    msgbox Amazon_Text_VillageStorage, MSGBOX_DEFAULT
    special ShowPokemonStorageSystemPC
    waitstate
    special SetHelpContextForMap
    releaseall
    end

Amazon_EventScript_StorageNeedsPartner::
    msgbox Amazon_Text_StorageNeedsPartner, MSGBOX_DEFAULT
    releaseall
    end

Amazon_Text_VillageStorage::
    .string "Posto de parceiros\p"
    .string "Guarde ou retire parceiros\n"
    .string "pelo PC da vila.$"

Amazon_Text_StorageNeedsPartner::
    .string "Escolha seu parceiro com\n"
    .string "a guia antes de usar o PC.$"
