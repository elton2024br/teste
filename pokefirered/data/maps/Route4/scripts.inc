Route4_MapScripts::
	.byte 0

Amazon_EventScript_PantanalAgent::
	lock
	faceplayer
	goto_if_unset FLAG_AMAZON_FOREST_STONE, Amazon_EventScript_PantanalLocked
	goto_if_set FLAG_AMAZON_FLOOD_STONE, Amazon_EventScript_PantanalDone
	goto_if_set FLAG_AMAZON_PANTANAL_AGENT_DEFEATED, Amazon_EventScript_PantanalReward
	trainerbattle_single TRAINER_BUG_CATCHER_COLTON_3, Amazon_Text_PantanalAgentIntro, Amazon_Text_PantanalAgentLoss
	setflag FLAG_AMAZON_PANTANAL_AGENT_DEFEATED
Amazon_EventScript_PantanalReward::
	checkitem ITEM_PEDRA_DAS_CHEIAS
	goto_if_eq VAR_RESULT, TRUE, Amazon_EventScript_PantanalMarkReward
	checkitemspace ITEM_PEDRA_DAS_CHEIAS, 1
	goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_PantanalFull
	additem ITEM_PEDRA_DAS_CHEIAS, 1
	goto_if_eq VAR_RESULT, FALSE, Amazon_EventScript_PantanalFull
Amazon_EventScript_PantanalMarkReward::
	setflag FLAG_AMAZON_FLOOD_STONE
	msgbox Amazon_Text_PantanalReward, MSGBOX_DEFAULT
	removeobject LOCALID_AMAZON_PANTANAL_AGENT
	release
	end
Amazon_EventScript_PantanalLocked::
	msgbox Amazon_Text_PantanalLocked, MSGBOX_DEFAULT
	release
	end
Amazon_EventScript_PantanalDone::
	msgbox Amazon_Text_PantanalDone, MSGBOX_DEFAULT
	release
	end
Amazon_EventScript_PantanalFull::
	msgbox Amazon_Text_PantanalFull, MSGBOX_DEFAULT
	release
	end

Amazon_Text_PantanalAgentIntro::
	.string "As cheias serao controladas.\n"
	.string "A última pedra é do Tio Sam!$"
Amazon_Text_PantanalAgentLoss::
	.string "As águas escolheram vocês...$"
Amazon_Text_PantanalReward::
	.string "Você recuperou a\n"
	.string "Pedra das Cheias!\p"
	.string "As cinco pedras foram reunidas!\p"
	.string "O caminho às Terras Raras\n"
	.string "pode ser aberto ao leste.$"
Amazon_Text_PantanalLocked::
	.string "A força da Mata Atlântica\n"
	.string "ainda nao acompanha vocês.$"
Amazon_Text_PantanalDone::
	.string "As cinco pedras ficaram seguras.\n"
	.string "Busque as Terras Raras ao leste.$"
Amazon_Text_PantanalFull::
	.string "Abra espaço nos itens especiais\n"
	.string "e volte para receber a pedra.$"

Amazon_EventScript_EnterRareLands::
	goto_if_unset FLAG_AMAZON_FLOOD_STONE, Amazon_EventScript_PantanalLocked
	warp MAP_CERULEAN_CITY, 5, 9
	waitstate
	end

Route4_EventScript_Unused::
	end

Route4_EventScript_Woman::
	msgbox Route4_Text_TrippedOverGeodude, MSGBOX_NPC
	end

Route4_EventScript_MtMoonSign::
	msgbox Route4_Text_MtMoonEntrance, MSGBOX_SIGN
	end

Route4_EventScript_RouteSign::
	msgbox Route4_Text_RouteSign, MSGBOX_SIGN
	end
