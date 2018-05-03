import pprint
import re
import sys
import match_func


findaddr = ['경기도 고양','경기도 성남','경기도 수원','경기도 안산','경기도 안양',
            '경기도 용인','경상남도 창원','경상북도 포항','전라북도 전주','충청남도 천안',
            '충청북도 청주']

for  i in range(201700,201800,100):
    for j in range(12,13):
        p_data = list(match_func.fetch_data(i+j))
        missrate = 0
        miss_addr = 0
        print('current month : '+str(i+j))
        before_res = ''
        before_addr = ''
        before_addr_str = ''
        for h in range(0,len(p_data)):
            p_data[h] = list(p_data[h])

            if before_addr == p_data[h][0]:
                res = before_res
                addr_str = before_addr_str
            else:
                before_addr = p_data[h][0]
                hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3\d]+')
                p_data[h][0] = hangul.sub('', p_data[h][0])
                addr_str = p_data[h][0]

                for q in range(0,len(findaddr)):
                    if addr_str.find('경상북도 영천시 신령면') == 0 :
                        addr_str = addr_str.replace('령','녕')
                        break
                    strindexing = addr_str.find(findaddr[q])

                    if strindexing == 0 :
                        addr_str = addr_str.replace(findaddr[q],findaddr[q]+'시 ')
                        # print('hi',addr_str)

                        if q == 10 and (addr_str[9:15] == '상당구 북문' or addr_str[9:15] == '상당구 남문'):
                            addr_str = addr_str.replace('동','')

                        break
                # match_func.program_exit()
                res = match_func.code_match(addr_str)
                before_res = res
                before_addr_str = addr_str

            # match_func.program_exit()
            if res == 0:
                miss_addr += 1
                logtxt = 'missAddress = '+str(i+j)+' / addr = ' +addr_str+ ' / index = '+str(h)
                print(logtxt)
                #match_func.write_log(logtxt)
                continue

            first = match_func.bunji_match(res,p_data[h])
            if len(first) == 0:
                missrate += 1
            p_data[h].append(res[:5])
            p_data[h].append(res[5:])
            p_data[h][7] = str(p_data[h][7])
            p_data[h][8] = str(p_data[h][8])
            for o in range(0,3):
                bbbun = ''
                jjji = ''
                if len(first) >= o+1:
                    bbbun = first[o][0]
                    jjji = first[o][1]
                p_data[h].append(bbbun)
                p_data[h].append(jjji)

        match_func.fuck_data(p_data)
        logtxt = 'index = '+str(i+j)+' / '+ str(h) +'totalinsert = '+str(len(p_data))+' misscount = '+missrate+' hitrate = '+str((len(p_data)-missrate)/len(p_data))
        print(logtxt)
        match_func.write_log(logtxt)
        match_func.program_exit()
