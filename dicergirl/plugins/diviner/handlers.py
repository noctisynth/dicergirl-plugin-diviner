from pathlib import Path

from uvdiviner.divine import quick_check, make_trigram
from uvdiviner.evolution import trigram, diagram
from uvdiviner.main import get_useful_data
from uvdiviner import colorize

from nonebot.matcher import Matcher
from nonebot.adapters import Bot as Bot, Event

from dicergirl.utils.handlers import get_user_card
from dicergirl.utils.formatters import format_msg
from dicergirl.handlers.on import on_startswith

from multilogging import multilogger
from .utils import (
    reset_limit,
    minus_limit,
    get_limit,
    has_user,
    set_user,
    get_groups,
    get_users,
)

import nonebot
import asyncio


DEBUG = False
colorize.disable()
current_dir = Path(__file__).resolve().parent
logger = multilogger(name="DicerGirl", payload="diviner")


divinecommand = on_startswith((".divine", ".div", ".dv"), priority=2, block=True).handle()
dqccommand = on_startswith((".dqc", ".qca", ".aqc"), priority=2, block=True).handle()


async def helphandler(matcher: Matcher):
    await matcher.send(
        "Unvisitor Diviner 使用帮助:\n" ".divine/.div 标准占卜\n" ".dqc/.qca 快速吉凶检定\n"
    )


async def divine(matcher: Matcher):
    global DEBUG

    await matcher.send(
        "天何言哉，叩之即应；神之灵矣，感而遂通。\n" "今有某人，有事关心，罔知休咎，罔释厥疑，\n" "惟神惟灵，望垂昭报，若可若否，尚明告之。"
    )
    logger.warning(
        "天何言哉，叩之即应；神之灵矣，感而遂通。\n" "今有某人，有事关心，罔知休咎，罔释厥疑，\n" "惟神惟灵，望垂昭报，若可若否，尚明告之。"
    )
    trigrams = (
        [
            make_trigram(),
            make_trigram(),
            make_trigram(),
        ]
        if not DEBUG
        else [
            trigram(8),
            trigram(8),
            trigram(6),
        ]
    )

    for _ in range(1, 28):
        if not DEBUG:
            await asyncio.sleep(1)

    await matcher.send("某宫三象，吉凶未判，再求外象三爻，以成一卦，以决忧疑。")
    logger.warning("某宫三象，吉凶未判，再求外象三爻，以成一卦，以决忧疑。")

    for _ in range(28, 56):
        if not DEBUG:
            await asyncio.sleep(1)

    trigrams += (
        [make_trigram(), make_trigram(), make_trigram()]
        if not DEBUG
        else [trigram(9), trigram(8), trigram(8)]
    )

    if not DEBUG:
        await asyncio.sleep(1)

    dia = diagram(trigrams)

    static, variable, result = get_useful_data(dia)

    if not static["卦名"] == variable["卦名"]:
        await matcher.send("占卜结果: " + static["卦名"][:-1] + "之" + variable["卦名"][:-1])
        logger.info("占卜结果: " + static["卦名"][:-1] + "之" + variable["卦名"][:-1])
    else:
        await matcher.send("占卜结果: " + static["卦名"])
        logger.info("占卜结果: " + static["卦名"])

    if not DEBUG:
        await asyncio.sleep(1)

    await matcher.send("本卦: " + static["卦名"] + "\n" + "卦辞: " + static["卦辞"])
    logger.info("本卦: " + static["卦名"] + "\n" + "卦辞: " + static["卦辞"])

    if not DEBUG:
        await asyncio.sleep(1)

    if dia.variated != 0:
        await matcher.send(
            "变卦:"
            + variable["卦名"]
            + "\n   卦辞: "
            + variable["卦辞"]
            + "\n"
            + "变爻数:"
            + str(dia.variated)
        )
        logger.info(
            "变卦:"
            + variable["卦名"]
            + "\n   卦辞: "
            + variable["卦辞"]
            + "\n"
            + "变爻数:"
            + str(dia.variated)
        )

    if not DEBUG:
        await asyncio.sleep(2)

    await matcher.send(result)
    logger.info(result)


async def divine_handler(matcher: Matcher, event: Event):
    args = format_msg(event.get_message(), begin=(".divine", ".div"))
    if len(args) != 0:
        if args[0] in ("help", "h"):
            await helphandler(matcher=matcher)
            return
        else:
            reason = args[0]
    else:
        reason = ""

    logger.warning("用户尝试发起一场占卜.")
    if not has_user(event):
        set_user(event)

    if get_limit(event) <= 0 and not DEBUG:
        await matcher.send("今日占卜次数已达安全上限, 欧若可拒绝继续进行占卜.")
        logger.warning("今日占卜次数已达安全上限, 欧若可拒绝继续进行占卜.")
        return

    minus_limit(event)
    await matcher.send(
        f"[{get_user_card(event)}]{f'由于[{reason}]' if reason else '发起'}]占卜.\n请注意, 本次占卜可能消耗一些时间, 请耐心等待."
    )
    await asyncio.sleep(1)
    await divine(matcher)
    logger.success("占卜完成.")


async def dqc_handler(matcher: Matcher, event: Event):
    logger.warning("用户尝试发起一场快速占卜检定.")
    if not has_user(event):
        set_user(event)

    args = format_msg(event.get_message(), begin=(".dqc", ".qca", ".aqc"))
    if len(args) != 0:
        if args[0] in ("help", "h"):
            await helphandler(matcher=matcher)
            return
        else:
            reason = args[0]
    else:
        reason = ""

    if get_limit(event) <= 0 and not DEBUG:
        await matcher.send("今日占卜次数已达安全上限, 欧若可拒绝继续进行占卜.")
        logger.warning("今日占卜次数已达安全上限, 欧若可拒绝继续进行占卜.")
        return

    minus_limit(event)
    qc = quick_check()
    result = str(qc)
    await matcher.send(
        f"[{get_user_card(event)}]{f'由于[{reason}]' if reason else ''}占卜得到卦象[{qc.name}], 快速检定[{result}]"
    )
    logger.info(f"卦象: {qc.name}\n占卜快速检定结果: {result}")
    logger.success("快速检定完成.")


commands = {
    "divinecommand": "divine_handler",
    "dqccommand": "dqc_handler",
}
