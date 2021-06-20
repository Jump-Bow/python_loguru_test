import datetime

import chardet
import loguru
import requests

def main():
    resp = requests.get('https://www.taifex.com.tw/cht/9/futuresQADetail')
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

    txt = None
    # 對 HTTP / HTTPS 回應的二進位原始內容進行編碼判斷
    det = chardet.detect(resp.content)
    # 捕捉編碼轉換例外錯誤
    try:
        # 若判斷結果信心度超過 0.5
        if det['confidence'] > 0.5:
            # 若編碼判斷是 BIG5
            if det['encoding'] == 'big-5':
                # 因 Python 的 BIG5 編碼標示為 big5，
                # 而非 chardet 回傳的 big-5，故需另外處理
                txt = resp.content.decode('big5')
            else:
                txt = resp.content.decode(det['encoding'])
        else:
            # 若判斷信心度不足，則嘗試使用 UTF-8 解碼
            txt = resp.content.decode('utf-8')
    except Exception as e:
        # 解碼失敗
        loguru.logger.error(e)

    # 解碼失敗無法取得有效文字內容資料
    if txt is None:
        return

    loguru.logger.info(txt)

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    main()