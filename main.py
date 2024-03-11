import asyncio
import time
import logging

from config.config import api_id, api_hash, session_name
from servises.meta_trade_functionality import MetaTradeMain
from servises.tg_chanel_parser import GetTGMessageChanel
import MetaTrader5 as mt5
from config.config import company, server, login, password




def check_and_write_text(text):
    filename = 'text_file.txt'
    with open(filename, 'r') as file:
        file_content = file.read()
        if text in file_content:
            return True

    with open(filename, 'a') as file:
        file.write(text)
        print("Текст додано до файлу.")


async def main():
    # ------------ tg pars ---------------
    await tg_client.connect_tg_client()  # connection to the telegram client
    await tg_client.connect_tg_channel()  # connection to the telegram channel
    mess = await tg_client.get_message()  # getting message from tg channel
    if check_and_write_text(mess):
        return

        # ------------ mt5 buy or sell ---------------
    await mt_user.create_symbol_and_info(tg_client.message_lst)
    await mt_user.check_open_symbol()
    await mt_user.create_other_params(tg_client.message_lst, tg_client.message)
    await mt_user.generate_json()
    await mt_user.send_json_trading()
    await mt_user.check_result_offer()


if __name__ == "__main__":
    mt_user = MetaTradeMain(mt5)  # creating an instance of the MetaTrader5 class
    tg_client = GetTGMessageChanel(session_name, api_id, api_hash)  # creating an instance of the Telegram class

    while True:
        time.sleep(3)
        res = asyncio.run(main())
