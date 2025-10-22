上から順(物件)にliが1から5まで増えていき、次にulが1増えてまたliが1から始まる。
li: 1~5 -> ul += 1
//*[@id="js-bukkenList"]/ul[1]/li[1]/div/div[2]/table
//*[@id="js-bukkenList"]/ul[1]/li[2]/div/div[2]/table
・・・
//*[@id="js-bukkenList"]/ul[1]/li[5]/div/div[2]/table
ここでulを2に変更
//*[@id="js-bukkenList"]/ul[2]/li[1]/div/div[2]/table
50件表示の場合はul[10]/li[5]まで行く

部屋ごとはtbodyの値が増えていく(tbodyは上限ない?)
//*[@id="js-bukkenList"]/ul[5]/li[1]/div/div[2]/table/tbody[1]/tr/td[9]/a
//*[@id="js-bukkenList"]/ul[5]/li[1]/div/div[2]/table/tbody[2]/tr/td[9]/a
//*[@id="js-bukkenList"]/ul[5]/li[1]/div/div[2]/table/tbody[7]/tr/td[9]/a

https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&sc=13300&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09

https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&sc=13300&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&page=2