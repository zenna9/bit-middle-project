from calendar import day_name
import jinja2
import pandas as pd
import numpy as np
import random
from pathlib import Path
from eat.models import diet
from django.db.models import Sum

DB_DIR = Path(__file__).resolve().parent.parent

# 성균: sql연동전이며 그전까지 랜덤매뉴의 연산으로 대체함
def recommend_food(request,date):
    idx = request.session['idx']
    
    # 영양DB와 분류정보 음식명 일치
    df_nDB = pd.read_csv(DB_DIR /'analysis_photo/yolo/nutrient_DB.csv',dtype=str)

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

    sum_tan = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('tan'))
    sum_ji= diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('ji'))
    sum_dan= diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('dan'))
    sum_kalsum = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('kalsum'))
    sum_inn = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('inn'))
    sum_kalum = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('kalum'))
    sum_magnesum = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('magnesum'))
    sum_chul = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('chul'))
    sum_ayeon = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('ayeon'))
    
    tan=list(sum_tan.values())[0]
    ji=list(sum_ji.values())[0]
    dan=list(sum_dan.values())[0]
    kalsum=list(sum_kalsum.values())[0]
    inn=list(sum_inn.values())[0]
    kalum=list(sum_kalum.values())[0]
    magnesum=list(sum_magnesum.values())[0]
    chul=list(sum_chul.values())[0]
    ayeon=list(sum_ayeon.values())[0]

    eval_num=[tan,ji,dan,kalsum,inn,kalum,magnesum,chul,ayeon]
    eat_lst=[]
    for j in range(len(eval_num)):
        eat_percent=round(100*(float(eval_num[j])/recommend_Nlst[j]))
        eat_lst.append(eat_percent)    
    
    eval_np=np.array(eat_lst)
    asc_indice=np.argsort(eval_np)
        
    r1=Nlst_name[asc_indice[0]]
    r2=Nlst_name[asc_indice[1]]

    r1_recommend=data_df.sort_values(by=r1, ascending=False).groupby(r1).head()
    r2_recommend=data_df.sort_values(by=r2, ascending=False).groupby(r2).head()
    print(r1_recommend.columns)

    r1_recommend_p=r1_recommend.iloc[0][r1]
    r2_recommend_p=r2_recommend.iloc[0][r2]
    
    recommend_data= {'LackN': f'{r1}, {r2}', 'recommendFoods': f'{r1_recommend.index[0]}({r1}:{r1_recommend_p}%), {r2_recommend.index[0]}({r2}:{r2_recommend_p}%)'}

    return recommend_data