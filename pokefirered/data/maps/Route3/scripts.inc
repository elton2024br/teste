Route3_MapScripts::
	.byte 0

Amazon_EventScript_AtlanticAgent::
	lock
	faceplayer
	goto_if_unset FLAG_AMAZON_DROUGHT_STONE, Amazon_EventScript_AtlanticLocked
	goto_if_set FLAG_AMAZON_FOREST_STONE, Amazon_EventScript_AtlanticDone
	goto_if_set FLAG_AMAZON_ATLANTIC_AGENT_DEFEATED, Amazon_EventScript_AtlanticReward
	trainerbattle_single TRAINER_BUG_CATCHER_COLTON_2, Amazon_Text_AtlanticAgentIntro, Amazon_Text_AtlanticAgentLoss
	setflag FLAG_AMAZON_ATLANTIC_AGENT_DEFEATED
Amazon_EventScript_AtlanticReward::
	checkitem ITEM_PEDRA_DA_MATA
	goto_if_eq VAR_RESULT, TRUE, Amazon_EventScript_AtlanticMarkReward
	checkitemspace ITEM_PEDRA_DA_MATA, 1
	goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_AtlanticFull
	additem ITEM_PEDRA_DA_MATA, 1
	goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_AtlanticFull
Amazon_EventScript_AtlanticMarkReward::
	setflag FLAG_AMAZON_FOREST_STONE
	msgbox Amazon_Text_AtlanticReward, MSGBOX_DEFAULT
	removeobject LOCALID_AMAZON_ATLANTIC_AGENT
	release
	end
Amazon_EventScript_AtlanticLocked::
	msgbox Amazon_Text_AtlanticLocked, MSGBOX_DEFAULT
	release
	end
Amazon_EventScript_AtlanticDone::
	msgbox Amazon_Text_AtlanticDone, MSGBOX_DEFAULT
	release
	end
Amazon_EventScript_AtlanticFull::
	msgbox Amazon_Text_AtlanticFull, MSGBOX_DEFAULT
	release
	end

Amazon_Text_AtlanticAgentIntro::
	.string "A mata será aberta à força.\n"
	.string "A quarta pedra é do Tio Sam!$"
Amazon_Text_AtlanticAgentLoss::
	.string "A floresta protegeu vocês...$"
Amazon_Text_AtlanticReward::
	.string "Você recuperou a\n"
	.string "Pedra da Mata!\p"
	.string "Agora você tem quatro das\n"
	.string "cinco pedras.\p"
	.string "O último habitat fica a leste.$"
Amazon_Text_AtlanticLocked::
	.string "Resista à seca da Caatinga\n"
	.string "antes de entrar nesta mata.$"
Amazon_Text_AtlanticDone::
	.string "A Pedra da Mata está segura.\n"
	.string "Siga para o último habitat.$"
Amazon_Text_AtlanticFull::
	.string "Abra espaço nos itens especiais\n"
	.string "e volte para receber a pedra.$"

Amazon_EventScript_EnterPantanal::
	goto_if_unset FLAG_AMAZON_FOREST_STONE, Amazon_EventScript_AtlanticLocked
	warp MAP_ROUTE4, 5, 9
	waitstate
	end

Route3_EventScript_Youngster::
	msgbox Route3_Text_TunnelFromCeruleanTiring, MSGBOX_NPC
	end

Route3_EventScript_RouteSign::
	msgbox Route3_Text_RouteSign, MSGBOX_SIGN
	end
