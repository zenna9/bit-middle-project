import pandas as pd
import numpy as np
import random

# 성균: sql연동전이며 그전까지 랜덤매뉴의 연산으로 대체함
def recommend_food():
    # 영양DB와 분류정보 음식명 일치
    db_file='E:/food_dataset1/음식 이미지 및 영양정보 텍스트/칼로리데이터셋/영양DB.csv'
    df_nDB = pd.read_csv(db_file,dtype=str)

    N_DB_lst=df_nDB.values.tolist()
    
    for i in range(len(N_DB_lst)):
        for j in range(len(N_DB_lst[i])):
            if N_DB_lst[i][j] =='-':
                N_DB_lst[i][j] ='0.00'

    recommend_tan_3=500
    # recommend_dang_4=0.001
    recommend_ji_5=40
    recommend_dan_6=70
    recommend_kalsum_7=700
    recommend_inn_8=700
    recommend_salt_9=20000
    recommend_kalum_10=3500
    recommend_magnesum_11=220
    recommend_cul_12=15
    recommend_ayeon_13=12

    recommend_Nlst=[recommend_tan_3,recommend_ji_5,recommend_dan_6,recommend_kalsum_7,
                    recommend_inn_8,recommend_kalum_10,recommend_magnesum_11,recommend_cul_12,recommend_ayeon_13]
    Nlst_name=['탄','지','단','칼슘','인','칼륨','마그네슘','철','아연']

    eval_lst=[[] for i in N_DB_lst]
    for i in range(len(N_DB_lst)):
        eval=[N_DB_lst[i][0]]+N_DB_lst[i][3:4]+N_DB_lst[i][5:9]+N_DB_lst[i][10:14]
        eval_lst[i].append(eval[0])
        eval_num=eval[1:]
        for j in range(len(eval_num)):
            eval_percent=round((100*(float(eval_num[j])/recommend_Nlst[j])),2)
            eval_lst[i].append(eval_percent)
    
    data_array=[]
    title=['']+Nlst_name
    data_array.append(title)
    data_array.extend(eval_lst)
    np_array=np.array(data_array)


    row_indices = np_array[1:, 0]
    column_names = np_array[0, 1:]
    data_df = pd.DataFrame(
        data=(np_array[1:, 1:]), index=row_indices, columns=column_names)
    
    input=random.randrange(1,401)
    eatN=eval_lst[input]
    eatNf= eatN[1:]
    lackNf_percent=[round(100-eatNf[i]) for i in range(len(eatNf))]
    lackNf_dec=sorted(lackNf_percent)
    lackNf_dec.reverse()
    f_rank=[]
    for i in lackNf_percent:
        f_rank.append(lackNf_dec.index(i)+1)

    r1_index=lackNf_percent.index(lackNf_dec[0])
    r2_index=lackNf_percent.index(lackNf_dec[1])

    r1=Nlst_name[r1_index]
    r2=Nlst_name[r2_index]

    r1_recommend=data_df.sort_values(by=r1, ascending=False).groupby(r1).head()
    r2_recommend=data_df.sort_values(by=r2, ascending=False).groupby(r2).head()

    eatNfr=[round(eatNf[i]) for i in range(len(eatNf))]
    
    nameAndEatNf=f'{Nlst_name[0]}({eatNfr[0]}), {Nlst_name[1]}({eatNfr[1]}), {Nlst_name[2]}({eatNfr[2]})'
    nameAndLackNf=f'{Nlst_name[0]}({lackNf_percent[0]}), {Nlst_name[1]}({lackNf_percent[1]}), {Nlst_name[2]}({lackNf_percent[2]})'
    recommend_data= {'nameAndEatNf': nameAndEatNf, 'nameAndLackNf': nameAndLackNf, 'lackNf_dec':r1+', '+r2, 'recommend_p':r1_recommend.index[0]+', '+r2_recommend.index[0]}

    return recommend_data