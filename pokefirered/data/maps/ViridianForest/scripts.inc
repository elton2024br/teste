ViridianForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ViridianForest_AmazonTransition
	.byte 0

ViridianForest_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_VIRIDIAN_FOREST
	end

ViridianForest_EventScript_Youngster::
	msgbox ViridianForest_Text_FriendsItchingToBattle, MSGBOX_NPC
	end

ViridianForest_EventScript_Boy::
	msgbox ViridianForest_Text_RanOutOfPokeBalls, MSGBOX_NPC
	end

ViridianForest_EventScript_TrainerTips1::
	msgbox ViridianForest_Text_AvoidGrassyAreasWhenWeak, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips2::
	msgbox ViridianForest_Text_UseAntidoteForPoison, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips3::
	msgbox ViridianForest_Text_ContactOakViaPCToRatePokedex, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips4::
	msgbox ViridianForest_Text_CantCatchOwnedMons, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips5::
	msgbox ViridianForest_Text_WeakenMonsBeforeCapture, MSGBOX_SIGN
	end

ViridianForest_EventScript_ExitSign::
	msgbox ViridianForest_Text_LeavingViridianForest, MSGBOX_SIGN
	end

ViridianForest_EventScript_Rick::
	trainerbattle_single TRAINER_BUG_CATCHER_RICK, ViridianForest_Text_RickIntro, ViridianForest_Text_RickDefeat
	msgbox ViridianForest_Text_RickPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Doug::
	trainerbattle_single TRAINER_BUG_CATCHER_DOUG, ViridianForest_Text_DougIntro, ViridianForest_Text_DougDefeat
	msgbox ViridianForest_Text_DougPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Sammy::
	trainerbattle_single TRAINER_BUG_CATCHER_SAMMY, ViridianForest_Text_SammyIntro, ViridianForest_Text_SammyDefeat
	msgbox ViridianForest_Text_SammyPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Anthony::
	trainerbattle_single TRAINER_BUG_CATCHER_ANTHONY, ViridianForest_Text_AnthonyIntro, ViridianForest_Text_AnthonyDefeat
	msgbox ViridianForest_Text_AnthonyPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Charlie::
	trainerbattle_single TRAINER_BUG_CATCHER_CHARLIE, ViridianForest_Text_CharlieIntro, ViridianForest_Text_CharlieDefeat
	msgbox ViridianForest_Text_CharliePostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_AmazonTransition::
	setflag FLAG_TEMP_1
	setrespawn HEAL_LOCATION_PALLET_TOWN
	call_if_set FLAG_AMAZON_BLOCKADE_DISABLED, Amazon_EventScript_OpenBridge
	end

Amazon_EventScript_OpenBridge::
    setmetatile 11, 10, 0x11, 0
    setmetatile 12, 10, 0x11, 0
    return
Amazon_EventScript_Agent::
    lock
    faceplayer
    goto_if_set FLAG_AMAZON_AGENT_DEFEATED, Amazon_EventScript_AgentDone
    trainerbattle_single TRAINER_BUG_CATCHER_RICK, Amazon_Text_AgentIntro, Amazon_Text_AgentLoss
    setflag FLAG_AMAZON_AGENT_DEFEATED
Amazon_EventScript_AgentDone::
    msgbox Amazon_Text_AgentDone, MSGBOX_DEFAULT
    release
    end
Amazon_EventScript_Control::
    lockall
    goto_if_unset FLAG_AMAZON_AGENT_DEFEATED, Amazon_EventScript_ControlLocked
    goto_if_set FLAG_AMAZON_BLOCKADE_DISABLED, Amazon_EventScript_ControlDone
    setflag FLAG_AMAZON_BLOCKADE_DISABLED
    call Amazon_EventScript_OpenBridge
    special DrawWholeMapView
Amazon_EventScript_ControlDone::
    msgbox Amazon_Text_ControlDone, MSGBOX_DEFAULT
    releaseall
    end
Amazon_EventScript_ControlLocked::
    msgbox Amazon_Text_ControlLocked, MSGBOX_DEFAULT
    releaseall
    end
Amazon_EventScript_Stone::
    lockall
    goto_if_unset FLAG_AMAZON_BLOCKADE_DISABLED, Amazon_EventScript_ControlLocked
    checkitem ITEM_PEDRA_DAS_AGUAS
    goto_if_eq VAR_RESULT, TRUE, Amazon_EventScript_StoneMark
    checkitemspace ITEM_PEDRA_DAS_AGUAS, 1
    goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_StoneFull
    additem ITEM_PEDRA_DAS_AGUAS, 1
    goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_StoneFull
Amazon_EventScript_StoneMark::
    setflag FLAG_AMAZON_WATER_STONE
    removeobject LOCALID_AMAZON_STONE
    msgbox Amazon_Text_StoneReceived, MSGBOX_DEFAULT
    releaseall
    end
Amazon_EventScript_StoneFull::
    msgbox Amazon_Text_StoneFull, MSGBOX_DEFAULT
    releaseall
    end
Amazon_Text_AgentIntro::
    .string "Este rio pertence ao Tio Sam!\p"
    .string "Ninguém passa sem nossa ordem!$"
Amazon_Text_AgentLoss::
    .string "Vocês venceram desta vez...$"
Amazon_Text_AgentDone::
    .string "O controle da máquina está ali.\n"
    .string "Pode desligar... eu desisto.$"
Amazon_Text_ControlLocked::
    .string "O agente protege o controle.\n"
    .string "Enfrente-o antes de passar.$"
Amazon_Text_ControlDone::
    .string "A máquina parou!\p"
    .string "Uma passagem segura foi aberta.\n"
    .string "Siga para a margem ao norte.$"
Amazon_Text_StoneReceived::
    .string "Você encontrou a Pedra das Águas!\p"
    .string "A primeira das cinco pedras.\n"
    .string "Volte e conte para a comunidade!$"
Amazon_Text_StoneFull::
    .string "Abra espaço nos itens especiais\n"
    .string "e volte para buscar a pedra.$"
