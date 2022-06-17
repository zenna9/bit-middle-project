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
    Nlst_name=['탄수화물','지방','단백질','칼슘','인','칼륨','마그네슘','철','아연']

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

    r1_recommend_p=r1_recommend.iloc[0][r1]
    r2_recommend_p=r2_recommend.iloc[0][r2]
    
    comments={'탄수화물':'우리 몸에 꼭 필요한 필수 에너지원이지만, 다이어트 등으로 탄수화물이 부족한 상태라면 지방에 이어 단백질 소비가 증가해 근육 약화, 피로, 스트레스, 두통 등을 유발하기 쉽습니다. 탄수화물의 섭취는 현미, 보리, 귀리 등 통곡물을 자주 먹는 게 좋고 식이섬유가 풍부한 과일 등에도 좋은 탄수화물이 풍부합니다. 반면에 당류, 정제곡물은 절제하는 것이 좋습니다.',
              '지방':'우리 몸에 꼭 필요한 필수 에너지원이지만, 다이어트 등으로 지방이 부족한 상태라면 지용성 비타민 (A, D, E, K) 의 결핍, 피부 건조, 탈모, 면역 시스템 저하 등의 이상이 발생할 수 있습니다. 가공식품에서 주로 함유된 트랜스지방을 피하고, 불포화 지방이 풍부한 고등어, 정어리, 연어, 굴, 아보카도, 올리브오일, 그리고 호두를 비롯한 견과류를 권장합니다.',
              '단백질':'단백질은 근육의 재료일 뿐 아니라, 면역력의 원천입니다. 단백질을 충분히 섭취하지 않으면 근육 약화, 근육량 감소, 관절 약화등의 이상이 발생할 수 있습니다. 단백질 보충용 건강기능식품보다 동·식물성 단백질 식품을 음식으로 골고루 섭취하는 것이 중요합니다.',
              '칼슘':'칼슘이 부족하게 되면 아이의 경우 성장이 더뎌지게 되고, 성인은 골다공증 등 뼈 질환을 유발할 수 있습니다. 그러나 칼슘이 너무 과하게 되면 위장장애를 일으킬 수 있습니다. 때문에 영양제 보충과 같이 권장량을 한꺼번에 먹는것 보다 유제품, 콩, 두부, 등푸른 생선, 다시마, 건새우, 멸치 등의 음식을 단백질, 비타민D와 함께 섭취하는것이 좋습니다.',
              '인':'우리 몸은 인을 사용하여 뼈를 튼튼하고 건강하게 유지합니다. 인은 또한 노폐물을 제거하고 손상된 조직을 복구하는데 도움이 됩니다. 대부분의 식단에서 충분한 인을 섭취할수 있지만, 혈당과 관련된 성인병을 가지고 있는 사람에게 인 결핍증상이 잘 나타날 수 있습니다. 단백질이 풍부한 고기류, 해물, 견과류, 씨앗, 요구르트 등을 통해 섭취하는것이 좋습니다.',
              '칼륨':'칼륨은 우리 몸 속의 나트륨과 균형을 이루며 정상 혈압을 유지하도록 도와주는 역할을 합니다. 또한 근육의 수축과 이완은 물론 심장 혈관 기능에도 중요한 역할을 담당하기 때문에 맵고 짠 음식을 즐겨 먹는 한국인에게 꼭 필요한 영양소입니다. 칼륨이 부족할 경우 몸의 피로, 현기증, 균형 이상 증상 등이 발생할 수 있습니다. 채소위주의 식단과 과일을 통해 섭취하세요.',
              '마그네슘': '마그네슘은 신경조직을 이완하여 긴장상태를 해소하고 안정을 찾는 데 도움을 주며, 포도당을 분해해 에너지원으로 이용하는 등 다양한 생화학적 반응에 꼭 필요합니다. 마그네슘이 결핍되면 근육 경련이나 불면증, 스트레스, 우울증 등과 같은 여러 건강 문제에 직면할 수 있기 때문에 주의해야 합니다. 현미, 시금치, 아보카도, 호박씨 초콜릿 등의 섭취를 통해 보충할 수 있습니다.',
              '철': '철분은 색소 단백질인 헤모글로빈 생산에 있어 가장 중요한 성분이며 헤모글로빈은 전신 조직에 산소를 공급하는 적혈구를 돕는 역할을 합니다. 철분이 부족할 경우 두통, 탈모, 피로, 하지불안 증후군 등을 유발할 수 있어 철분 부족을 막으려면 소고기, 해조류, 녹황색 채소, 비트, 감자 등의 음식을 섭취하는 것이 좋습니다.',
              '아연': '아연은 감기회복을 돕고, 혈당 수치를 조절하며, 심장 건강을 증진시키는데 도움을 줍니다. 아연을 지나치게 많이 섭취할 경우 메스꺼움, 구토, 설사 등과 같은 문제를 초래할 수 있지만, 부족 시에는 굴, 붉은 고기, 갑각류 해산물과 같은 음식을 통해 건강하게 섭취할 수 있습니다.'
    }
    comment=comments.get(r1)
    
    recommend_data= {'rComments': comment, 'lackN1':r1, 'lackN2':r2, 'recommendFoods': f'{r1_recommend.index[0]}({r1}:{r1_recommend_p}%), {r2_recommend.index[0]}({r2}:{r2_recommend_p}%)', 'r1': r1_recommend.index[0], 'r2': r2_recommend.index[0], 'N_percent': eat_lst[3:]}

    return recommend_data