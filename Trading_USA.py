
import yfinance as yf
import requests

def send_text(bot_message) :
    print(bot_message)
    bot_token = '5666620357:AAGlHeW1C7D7MOGeBqPtNX4KHxS6H_vbbtI'
    bot_ChatID = '5782658712'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_ChatID + \
        '&parse_mode=MarkdownV2&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

asset = ['^DJI','META','SONY','AAPL']
TableauActions = ['Dow Jones','Facebook','Sony','Apple','NFLX']
data = ['','','','','']
for i in range(len(asset)) :
    data[i] = yf.download(asset[i], period='1mo',interval='1h')
    high9 = data[i].High.rolling(9).max()
    Low9 = data[i].High.rolling(9).min()
    high26 = data[i].High.rolling(26).max() 
    Low26 = data[i].High.rolling(26).min()
    high52 = data[i].High.rolling(52).max()
    Low52 = data[i].High.rolling(52).min()
    data[i]['tenkan_sen'] = (high9 + Low9)/2
    data[i]['kijun_sen'] = (high26 +Low26)/2
    data[i]['SSA'] = ((data[i].tenkan_sen + data[i].kijun_sen)/2).shift(26)
    data[i]['SSB'] = ((high52 + Low52)/2).shift(26)
    data[i]['achat'] ='NON'
    data[i]['chikou'] = data[i].Close.shift(-26)

def Long() :
    for i in range(len(asset)):
        
        if data[i].Close[-1] > data[i].tenkan_sen[-1] and data[i].tenkan_sen[-1] >= data[i].kijun_sen[-1] and data[i].Close[-1] > data[i].SSA[-1] and data[i].Close[-1] > data[i].SSB[-1] and (data[i].chikou[-27] > data[i].SSB[-27] or data[i].chikou[-27] > data[i].SSA[-27]):
            data[i].achat[-1] = 'ACHAT'
        if data[i].Close[-2] > data[i].tenkan_sen[-2] and data[i].tenkan_sen[-2] >= data[i].kijun_sen[-2] and data[i].Close[-2] > data[i].SSA[-2] and data[i].Close[-2] > data[i].SSB[-2] and (data[i].chikou[-28] > data[i].SSB[-28] or data[i].chikou[-28] > data[i].SSA[-28]):
            data[i].achat[-2] = 'ACHAT'   
        if data[i].achat[-1] == 'ACHAT' and data[i].achat[-2] != 'ACHAT' :  
           send_text("Long du " + TableauActions[i] + " au prix de " +  str(data[i].Close[-1]).replace('.',','))   
        if data[i].achat[-1] != 'ACHAT' and data[i].achat[-2] == 'ACHAT' :
            send_text("Coupe ton LONG " + TableauActions[i] + " au prix de " + str(data[i].Close[-1]).replace('.',','))
def Short() :
    for i in range(len(asset))   :    
        if data[i].Close[-1] < data[i].tenkan_sen[-1] and data[i].tenkan_sen[-1] <= data[i].kijun_sen[-1] and data[i].Close[-1] < data[i].SSA[-1] and data[i].Close[-1] < data[i].SSB[-1] and (data[i].chikou[-27] < data[i].SSB[-27] or data[i].chikou[-27] < data[i].SSA[-27]):
            data[i].achat[-1] = 'SHORT'
        if data[i].Close[-2] < data[i].tenkan_sen[-2] and data[i].tenkan_sen[-2] <= data[i].kijun_sen[-2] and data[i].Close[-2] < data[i].SSA[-2] and data[i].Close[-2] < data[i].SSB[-2] and (data[i].chikou[-28] < data[i].SSB[-28] or data[i].chikou[-28] < data[i].SSA[-28]):
            data[i].achat[-2] = 'SHORT'      
        if data[i].achat[-1] == 'SHORT' and data[i].achat[-2] != 'SHORT' :    
            send_text("SHORT du " + TableauActions[i] + " au prix de " +  str(data[i].Close[-1]).replace('.',',')) 
        if data[i].achat[-1] != 'SHORT' and data[i].achat[-2] == 'SHORT' :
            send_text("Coupe ton SHORT " + TableauActions[i] + " au prix de " + str(data[i].Close[-1]).replace('.',','))
            # correspond à une notification de stopper le short 

Long()
Short()








