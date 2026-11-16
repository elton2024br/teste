Route2_MapScripts::
	.byte 0

Route2_EventScript_RouteSign::
	msgbox Route2_Text_RouteSign, MSGBOX_SIGN
	end

Route2_EventScript_DiglettsCaveSign::
	msgbox Route2_Text_DiglettsCave, MSGBOX_SIGN
	end

Amazon_EventScript_EnterCaatinga::
	goto_if_unset FLAG_AMAZON_ROOT_STONE, Amazon_EventScript_CerradoLocked
	warp MAP_PEWTER_CITY, 23, 38
	waitstate
	end

Amazon_EventScript_CerradoAgent::
	lock
	faceplayer
	goto_if_unset FLAG_AMAZON_WATER_STONE, Amazon_EventScript_CerradoLocked
	goto_if_set FLAG_AMAZON_ROOT_STONE, Amazon_EventScript_CerradoDone
	goto_if_set FLAG_AMAZON_CERRADO_AGENT_DEFEATED, Amazon_EventScript_CerradoReward
	trainerbattle_single TRAINER_BUG_CATCHER_DOUG, Amazon_Text_CerradoAgentIntro, Amazon_Text_CerradoAgentLoss
	setflag FLAG_AMAZON_CERRADO_AGENT_DEFEATED
Amazon_EventScript_CerradoReward::
	checkitem ITEM_PEDRA_DAS_RAIZES
	goto_if_eq VAR_RESULT, TRUE, Amazon_EventScript_CerradoMarkReward
	checkitemspace ITEM_PEDRA_DAS_RAIZES, 1
	goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_CerradoFull
	additem ITEM_PEDRA_DAS_RAIZES, 1
	goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_CerradoFull
Amazon_EventScript_CerradoMarkReward::
	setflag FLAG_AMAZON_ROOT_STONE
	special HealPlayerParty
	msgbox Amazon_Text_CerradoReward, MSGBOX_DEFAULT
	removeobject LOCALID_AMAZON_CERRADO_AGENT
	release
	end
Amazon_EventScript_CerradoLocked::
	msgbox Amazon_Text_CerradoLocked, MSGBOX_DEFAULT
	release
	end
Amazon_EventScript_CerradoDone::
	msgbox Amazon_Text_CerradoDone, MSGBOX_DEFAULT
	release
	end
Amazon_EventScript_CerradoFull::
	msgbox Amazon_Text_CerradoFull, MSGBOX_DEFAULT
	release
	end

Amazon_Text_CerradoAgentIntro::
	.string "As raízes deste campo agora\n"
	.string "pertencem ao Tio Sam!$"
Amazon_Text_CerradoAgentLoss::
	.string "A terra respondeu a vocês...$"
Amazon_Text_CerradoReward::
	.string "Você recuperou a\n"
	.string "Pedra das Raízes!\p"
	.string "Agora você tem duas das\n"
	.string "cinco pedras.\p"
	.string "A trilha continua ao norte.$"
Amazon_Text_CerradoLocked::
	.string "O rio ainda está bloqueado.\n"
	.string "Volte à floresta e liberte a água.$"
Amazon_Text_CerradoDone::
	.string "A Pedra das Raízes está segura.\n"
	.string "Continue pela trilha ao norte.$"
Amazon_Text_CerradoFull::
	.string "Abra espaço nos itens especiais\n"
	.string "e volte para receber a pedra.$"
