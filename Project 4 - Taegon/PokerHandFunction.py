import math

def madecalc(myHand, otherHand):




    # 0-1. 초기 처리
    Pbs=[] # 리턴할 리스트 (확률값들)
    deck =[] # 카드뭉치 list 생성.    flag 1 : 해당 카드가 카드뭉치 안에 있음, flag 2 : 해당 카드는 내가 가지고 있음, flag 3 : 해당 카드는 남이 가지고 있음
    deck.append(0) # 덱의 0번째는 0으로 처리, 1부터 유효한 인덱스
    my_cnt = len(myHand) # 내가 가진 패의 수
    other_cnt = len(otherHand) # 상대방이 가진 패의 수
    my_card = [] # 내가가진 카드 1~52
    other_card = [] # 다른사람이 가진 카드 1~52
    
    if(my_cnt < 7):
        player_cnt = int(other_cnt / (my_cnt-2)) + 1 # 나포함 플레이어 수
    else:
        player_cnt = int(other_cnt / 4) + 1

    #deck_cnt = int(52 - (my_cnt * player_cnt)) #덱에 남은 카드 수
    deck_cnt = int(52 - (my_cnt + other_cnt)) #덱에 남은 카드 수, 단 상대의 히든패도 여기에 포함
    turn = 7 - my_cnt
    total_case = math.comb(deck_cnt,turn)

    for i in range(52): # 카드뭉치 속 모든카드 flag : 1
        deck.append(1)

    # 0-2. 내패에 대한 처리    
    for card in myHand:
        if len(card) == 2:
            number = card[0]
            shape = card[1]
        else:
            number = card[0:2]
            shape = card[2]
        
        if number == "A":
            number = 1
        elif number == "K":
            number = 13
        elif number == "Q":
            number = 12
        elif number == "J":
            number = 11
        
        if shape == "S":
            number = int(number) + 13*0
        elif shape == "D":
            number = int(number) + 13*1
        elif shape == "H":
            number = int(number) + 13*2
        elif shape == "C":
            number = int(number) + 13*3
        
        deck[number] = 2 # 내가 보유한 카드는 덱에 2로 업데이트
        my_card.append(number)
    
    my_card.sort()

    # 0-3. 상대 패에 대한 처리
    for card in otherHand:
        if len(card) == 2:
            number = card[0]
            shape = card[1]
        else:
            number = card[0:2]
            shape = card[2]
        
        if number == "A":
            number = 1
        elif number == "K":
            number = 13
        elif number == "Q":
            number = 12
        elif number == "J":
            number = 11
        
        if shape == "S":
            number = int(number) + 13*0
        elif shape == "D":
            number = int(number) + 13*1
        elif shape == "H":
            number = int(number) + 13*2
        elif shape == "C":
            number = int(number) + 13*3
        
        deck[number] = 3 # 내가 보유한 카드는 덱에 2로 업데이트
        other_card.append(number)
    
    other_card.sort()

    #print("콤비네이션 테스트")
    #print(math.comb(45,2))

    ST_total_cards = [4,4,4,4,4,4,4,4,4,4,4,4,4] # A~K
    ST_my_cards = [0,0,0,0,0,0,0,0,0,0,0,0,0] #A~K
    ST_other_cards = [0,0,0,0,0,0,0,0,0,0,0,0,0] #A~K

    # 족보에 해당하는 카드가 나한테 있으면 카운드
    for i in range(13):
        for j in range(4):
            if(deck[i+1+(13*j)]==2):
                ST_my_cards[i]+=1
                ST_total_cards[i]-=1
            elif(deck[i+1+(13*j)]==3):
                ST_other_cards[i]+=1
                ST_total_cards[i]-=1



    # 1.로티플 확률
    RF_pr = 0
    RF_case = 0

    for i in range(4): # 4가지 문양별로 계산
        shape = 13*i
        my_have_cnt = 0 # 내가가진 족보 필요 카드 수
        need_cnt = 5    # 족보에 총 필요한 카드 수

        # 상대방이, 내가 필요한 카드를 하나라도 가지고 있으면 continue
        fail_flag = 0
        for j in range(other_cnt):   
            if(other_card[j] == shape+1 or (other_card[j] >= shape+10 and other_card[j] <= shape+13)):
                fail_flag=1
                break
        if(fail_flag==1):
            continue


        # 내가 가진 카드가 족보에 해당하면 카운트
        for j in range(my_cnt):   
            if(my_card[j] == shape+1 or (my_card[j] >= shape+10 and my_card[j] <= shape+13)):
                my_have_cnt+=1
                need_cnt-=1
        
        # 남은턴보다 필요카드가 많다면, continue
        if(need_cnt > turn): 
            continue
                                
        RF_case += math.comb(deck_cnt-need_cnt,turn-need_cnt)
        #print("덱카운트 : ",deck_cnt, ", 니트카운트 : ", need_cnt, ", 토탈케이스 : ", total_case, ", RSP케이스 : ", RF_case)

    RF_pr = round(RF_case / total_case * 100,4)
    print("로티플 확률은? : ",RF_pr,"%")
    Pbs.append(RF_pr)


    # 2.스티플 확률
    SF_pr = 0
    SF_case = 0

    for i in range(4): # 4가지 문양별로 계산
        shape = 13*i
        need_cards=[{0} for j in range(9)] # 필요 카드에 대한 set형 list, 1~9열은 스티플 시작 숫자, list안의 set은 해당 숫자로 시작하는 중 내가 가지고 있지 않은 필요카드 수
        complete_flag = 0

        for j in range(9): # 스티플 시작숫자 1~9            
            my_have_cnt = 0 # 내가가진 족보 필요 카드 수
            need_cnt = 5    # 족보에 총 필요한 카드 수

            # 상대방이, 내가 필요한 카드를 하나라도 가지고 있으면 continue
            fail_flag = 0
            for k in range(other_cnt):   
                if(other_card[k] >= shape+j+1 and other_card[k] <= shape+j+5):
                    fail_flag=1
                    break
            if(fail_flag==1):
                continue


            # 내가 가진 카드가 족보에 해당하면 카운트
            # j부터 시작하는 스티플족보에, 내가 가지지 않은 필요한 패를 temp에 추가
            temp = {0}
            temp.remove(0)
            for k in range(5):
                card_have=0
                for l in range(my_cnt):
                    if(my_card[l] == shape+j+k+1):
                        my_have_cnt+=1
                        need_cnt-=1
                        card_have=1
                        break
                if(card_have==0):
                    temp.add(j+k+1)
            

            # 남은턴보다 필요카드가 많다면, continue
            if(need_cnt > turn): 
                continue

            # 이미 완성이면 종료

            if(my_have_cnt >= 5):
                SF_case = total_case
                complete_flag = 1
                break

            # temp를 관리용 필요카드 list에 추가
            need_cards[j] = temp 

            #print(need_cards) # 테스트 코드

            # SP_case_mini 변수에, j부터 시작하는 스티플 족보의 경우의 수 계산하여 임시로 저장
            SP_case_mini = math.comb(deck_cnt-need_cnt,turn-need_cnt)
            
            # SP_case_mini 변수에 중복계산된 부분 처리 (관리용리스트 need_cards에서 부분집합 관계에 있는 부분 처리)
            for k in range(len(need_cards)):
                if(k == j) :
                    continue
                # j로시작하는 스티플 족보가 
                if(set.intersection(need_cards[j], need_cards[k]) == need_cards[j] and need_cards[k] != need_cards[j]):
                    SP_case_mini -= math.comb(deck_cnt-need_cnt-1,turn-need_cnt-1)
                    #테스트 코드
                    #print("=========")
                    #print(need_cards[j])
                    #print(need_cards[k])
                    break
                elif(set.intersection(need_cards[j], need_cards[k]) == need_cards[k]):
                    SP_case_mini = 0
                    break
                
            SF_case += SP_case_mini
            #print("덱카운트 : ",deck_cnt, ", 니트카운트 : ", need_cnt, ", 토탈케이스 : ", total_case, ", SP케이스 : ", SF_case)
        if(complete_flag==1):
            break
    
    SF_pr = round(SF_case / total_case * 100,4)
    print("스티플 확률은? : ",SF_pr,"%")
    #print("손으로 계산값 : ",math.comb(46,2)+math.comb(46,2)+math.comb(46,2))
    Pbs.append(SF_pr)


    # 3.포카드 확률
    FK_pr = 0
    FK_case = 0

    for i in range(13): #각 숫자별 포카드 될 확률 계산
        my_have_cnt = 0 # 내가가진 족보 필요 카드 수
        need_cnt = 4    # 족보에 총 필요한 카드 수        

        # 상대방이, 내가 필요한 카드를 하나라도 가지고 있으면 continue
        fail_flag = 0
        for j in range(other_cnt):   
            if((other_card[j]-1)%13+1 == i+1):
                fail_flag=1
                break
        if(fail_flag==1):
            continue

        # 내가 가진 카드가 족보에 해당하면 카운트
        for j in range(my_cnt):   
            if((my_card[j]-1)%13+1 == i+1):
                my_have_cnt+=1
                need_cnt-=1
        
        # 남은턴보다 필요카드가 많다면, continue
        if(need_cnt > turn): 
            continue

        FK_case += math.comb(deck_cnt-need_cnt,turn-need_cnt)
        
        #print("덱카운트 : ",deck_cnt, ", 니트카운트 : ", need_cnt, ", 토탈케이스 : ", total_case, ", FK케이스 : ", FK_case, "이번카드의 케이스 : ", math.comb(deck_cnt-need_cnt,turn-need_cnt))

    FK_pr = round(FK_case / total_case * 100,4)
    print("포카드 확률은? : ",FK_pr,"%")
    Pbs.append(FK_pr)


    # 4.풀하우스 확률
    FH_pr = 0
    FH_case = 0

    for i in range(13): # 각 숫자별 트리플 될 확률 계산
        FH_mini_max=0
        complete_flag = 0
        for j in range(13): # 각 숫자별 원페어 될 확률 계산 (i,j페어 확률계산)
            if(i==j):
                continue
            my_have_cnt1 = 0 # 내가가진 족보 필요 카드 수1
            need_cnt1 = 3    # 족보에 총 필요한 카드 수1
            my_have_cnt2 = 0 # 내가가진 족보 필요 카드 수2
            need_cnt2 = 2    # 족보에 총 필요한 카드 수2

            # 상대방이, 내가 필요한 카드를 각각 2,3장이상 가지고 있으면 continue
            if(ST_other_cards[i] >= 2 or ST_other_cards[j] >= 3):
                continue

            # 내가 가진 카드가 족보에 해당하면 카운트
            my_have_cnt1 = ST_my_cards[i]
            my_have_cnt2 = ST_my_cards[j]
            need_cnt1 = 3 - my_have_cnt1
            need_cnt2 = 2 - my_have_cnt2


            if(need_cnt1 <= 0 and need_cnt2 <= 0):
                FH_case = total_case
                complete_flag = 1
                break
            
            if(need_cnt1 <= 0):
                need_cnt1 = 0
            if(need_cnt2 <= 0):
                need_cnt2 = 0


            # 남은턴보다 필요카드가 많다면, continue
            if(need_cnt1+need_cnt2 > turn): 
                continue

            FH_mini = math.comb(4-ST_my_cards[i]-ST_other_cards[i],need_cnt1) * math.comb(4-ST_my_cards[j]-ST_other_cards[j],need_cnt2) * math.comb(deck_cnt-need_cnt1-need_cnt2,turn-need_cnt1-need_cnt2)
            if(FH_mini_max < FH_mini):
                FH_mini_max = FH_mini
        FH_case += FH_mini_max
        #print(i+1, "번 트리플 풀하우스 경우의 수 : ", FH_mini_max)
        


        if(complete_flag == 1):
            break
    
    FH_pr = round(FH_case / total_case * 100,4)
    print("풀하우스 확률은? : ",FH_pr,"%")
    Pbs.append(FH_pr)


    # 5.플러쉬 확률
    FS_pr = 0
    FS_case = 0
    
    for i in range(4): # 4가지 문양별로 계산
        shape = 13*i
        my_have_cnt = 0 # 내가가진 족보 필요 카드 수
        need_cnt = 5    # 족보에 총 필요한 카드 수
        total_card = 13

        # 내가 가진 카드가 족보에 해당되거나, 상대가 족보에 해당되는 카드를 가지고 있으면 처리
        for j in range(13):   
            if(deck[j+(13*i)+1] == 2):
                my_have_cnt+=1
                total_card-=1
                if(my_have_cnt>5):
                    continue                
                need_cnt-=1
            elif(deck[j+(13*i)+1] == 3):
                total_card-=1


        # 가져올 수 있는 카드보다 필요카드가 많다면, continue
        if(need_cnt > total_card):
            continue

        # 남은턴보다 필요카드가 많다면, continue
        if(need_cnt > turn): 
            continue

        FS_case += math.comb(total_card,need_cnt) * math.comb(deck_cnt-need_cnt,turn-need_cnt)
        #print("덱카운트 : ",deck_cnt, ", 니트카운트 : ", need_cnt, ", 토탈케이스 : ", total_case, ", FS케이스 : ", FS_case,"남은카드",total_card)
    
    FS_pr = round(FS_case / total_case * 100,4)
    print("플러쉬 확률은? : ",FS_pr,"%")
    Pbs.append(FS_pr)



    # 6.마운틴 확률
    MT_pr = 0
    MT_case = 0

    MT_my_have_cnt = 0 # 내가가진 족보 필요 카드 수
    MT_need_kind_cnt = 5 # 족보에 총 필요한 카드 수
    MT_need_cnt = 20 # 필요한 카드들이 남아 있는 개수
    MT_total_cards = [4,4,4,4,4] # 10, J, Q, K, A
    MT_my_cards = [0,0,0,0,0] # 10, J, Q, K, A


    # 족보에 해당하는 카드가 나한테 있으면 카운드
    for i in range(5):
        for j in range(4):
            if(deck[(i+9)%13+1+(13*j)]==2):
                MT_my_cards[i]+=1
                MT_total_cards[i]-=1
                MT_need_cnt-=1
            elif(deck[(i+9)%13+1+(13*j)]==3):
                MT_total_cards[i]-=1
                MT_need_cnt-=1

    for i in range(len(MT_my_cards)):
        if(MT_my_cards[i] != 0):
            MT_my_have_cnt+=1
            MT_need_kind_cnt-=1

    # 필요한 카드가 덱에 없으면 fail
    MT_fail_flag=0
    for i in range(len(MT_my_cards)):
        if(MT_my_cards[i] == 0 and MT_total_cards[i] == 0):
            MT_fail_flag==1

    # 남은턴이 필요카드 수보다 적으면 fail
    if(MT_need_kind_cnt > turn ):
        MT_fail_flag=1

    if(MT_fail_flag==0):
        temp=1
        for i in range(5):
            if(MT_my_cards[i] == 0):
                temp *= MT_total_cards[i]

        MT_case = temp * math.comb(deck_cnt-MT_need_kind_cnt,turn-MT_need_kind_cnt)

    MT_pr = round(MT_case / total_case * 100,4)
    print("마운틴 확률은? : ",MT_pr,"%")
    Pbs.append(MT_pr)

    

    # 7.백스트레이트 확률
    BS_pr = 0
    BS_case = 0

    BS_my_have_cnt = 0 # 내가가진 족보 필요 카드 수
    BS_need_kind_cnt = 5 # 족보에 총 필요한 카드 수
    BS_need_cnt = 20 # 필요한 카드들이 남아 있는 개수
    BS_total_cards = [4,4,4,4,4] # A, 2, 3, 4, 5
    BS_my_cards = [0,0,0,0,0] # A, 2, 3, 4, 5


    # 족보에 해당하는 카드가 나한테 있으면 카운드
    for i in range(5):
        for j in range(4):
            if(deck[i+1+(13*j)]==2):
                BS_my_cards[i]+=1
                BS_total_cards[i]-=1
                BS_need_cnt-=1
            elif(deck[i+1+(13*j)]==3):
                BS_total_cards[i]-=1
                BS_need_cnt-=1

    for i in range(len(BS_my_cards)):
        if(BS_my_cards[i] != 0):
            BS_my_have_cnt+=1
            BS_need_kind_cnt-=1

    # 필요한 카드가 덱에 없으면 fail
    BS_fail_flag=0
    for i in range(len(BS_my_cards)):
        if(BS_my_cards[i] == 0 and BS_total_cards[i] == 0):
            BS_fail_flag==1

    # 남은턴이 필요카드 수보다 적으면 fail
    if(BS_need_kind_cnt > turn):
        BS_fail_flag=1
    if(BS_fail_flag==0):
        temp=1
        for i in range(5):
            if(BS_my_cards[i] == 0):
                temp *= BS_total_cards[i]
        #print(deck_cnt,", ",BS_need_kind_cnt,", ",turn,", ",BS_need_kind_cnt)
        BS_case = temp * math.comb(deck_cnt-BS_need_kind_cnt,turn-BS_need_kind_cnt)

    BS_pr = round(BS_case / total_case * 100,4)
    print("백스트레이트 확률은? : ",BS_pr,"%")
    Pbs.append(BS_pr)



    
    # 8.스트레이트 확률
    ST_pr = 0
    ST_case = 0                

    ST_need_cards=[{0} for j in range(8)] # 필요 카드에 대한 set형 list, 1~9열은 스티플 시작 숫자, list안의 set은 해당 숫자로 시작하는 중 내가 가지고 있지 않은 필요카드 수
    for i in range(8): # 스트레이트 시작숫자 2~9 별로 계산

        ST_my_have_cnt = 0 # 내가가진 족보 필요 카드 수
        ST_need_kind_cnt = 5 # 족보에 총 필요한 카드 수
        ST_need_cnt = 20 # 필요한 카드들이 남아 있는 개수

        for j in range(5):
            for k in range(4):
                if(deck[j+i+2+(13*k)]==2):
                    ST_need_cnt-=1
                elif(deck[j+i+2+(13*k)]==3):
                    ST_need_cnt-=1


        for j in range(5):
            if(ST_my_cards[j+i+1] != 0):
                ST_my_have_cnt+=1
                ST_need_kind_cnt-=1


        
        # i부터 시작하는 스트레이트 족보에, 내가 가지지 않은 필요한 패를 temp에 추가
        temp = {0}
        temp.remove(0)
        for j in range(5):
            card_have=0
            for k in range(my_cnt):
                if((my_card[k]-1)%13+1 == i+j+2):
                    card_have=1
                    break
            if(card_have==0):
                temp.add(i+j+2)
        

        # 필요한 카드가 덱에 없으면 continue
        for j in range(5):
            if(ST_my_cards[i+j+1] == 0 and ST_total_cards[i+j+1] == 0):
                continue


        # 남은턴이 필요카드 수보다 적으면 continue
        if(ST_need_kind_cnt > turn):
            continue
        
        # temp를 관리용 필요카드 list에 추가
        ST_need_cards[i] = temp
        #print(ST_need_cards)
        
        # 이미 완성이면 종료
        if(ST_my_have_cnt >= 5):
            ST_case = total_case
            break

        temp=1
        for j in range(5):
            if(ST_my_cards[i+j+1] == 0):
                temp *= ST_total_cards[i+j+1]
        ST_case_mini = temp * math.comb(deck_cnt-ST_need_kind_cnt,turn-ST_need_kind_cnt)
        #print(ST_total_cards)
        #print(ST_my_cards)
        #print(temp)
        #print(ST_case_mini)



        # ST_case_mini 변수에 중복계산된 부분 처리 (관리용리스트 ST_need_cards에서 부분집합 관계에 있는 부분 처리)
        for j in range(len(ST_need_cards)):
            if(j == i) :
                continue
            # j로시작하는 스티플 족보가 
            if(set.intersection(ST_need_cards[i], ST_need_cards[j]) == ST_need_cards[i] and ST_need_cards[i] != ST_need_cards[j]):
                temp2=1
                for k in range(5):
                    if(ST_my_cards[i+k] == 0):
                        temp2 *= ST_total_cards[i+k]
                        #print("ST_my_cards[j+k] : ", ST_my_cards[j+k],",j,k는: ", j, ", ",k)
                        #print("temp2 : ", temp2)
                ST_case_mini -= temp2 * math.comb(deck_cnt-ST_need_kind_cnt-1,turn-ST_need_kind_cnt-1)
                #테스트 코드
                #print("=========")
                #print(need_cards[j])
                #print(need_cards[k])
                break
            elif(set.intersection(ST_need_cards[i], ST_need_cards[j]) == ST_need_cards[j]):
                ST_case_mini = 0
                break
            
        ST_case += ST_case_mini
        #print("덱카운트 : ",deck_cnt, ", 니트카운트 : ", need_cnt, ", 토탈케이스 : ", total_case, ", 이번 ST케이스 : ",ST_case_mini , "토탈 ST 케이스 : ", ST_case," ", i+2, "로시작하는 스트레이트")

    ST_pr = round(ST_case / total_case * 100,4)
    print("스트레이트 확률은? : ",ST_pr,"%")
    Pbs.append(ST_pr)


    # 9.트리플 확률
    TR_pr = 0
    TR_case = 0

    for i in range(13): # 각 숫자별 트리플 될 확률 계산
        my_have_cnt = 0 # 내가가진 족보 필요 카드 수
        need_cnt = 3    # 족보에 총 필요한 카드 수        

        # 상대방이, 내가 필요한 카드를 2장이상 가지고 있으면 continue
        if(ST_other_cards[i] >= 2):
            continue

        # 내가 가진 카드가 족보에 해당하면 카운트
        my_have_cnt = ST_my_cards[i]
        need_cnt = 3 - my_have_cnt
        if(need_cnt <= 0):
            TR_case = total_case
            break
        
        # 남은턴보다 필요카드가 많다면, continue
        if(need_cnt > turn): 
            continue
        #print(i+1,"트리플 경우의 수 : ", math.comb(4-ST_my_cards[i]-ST_other_cards[i],need_cnt) * math.comb(deck_cnt-need_cnt,turn-need_cnt))
        TR_case += math.comb(4-ST_my_cards[i]-ST_other_cards[i],need_cnt) * math.comb(deck_cnt-need_cnt,turn-need_cnt)
        #print("덱카운트 : ",deck_cnt, ", 니트카운트 : ", need_cnt, ", 토탈케이스 : ", total_case, ", TR케이스 : ", TR_case, "이번카드의 케이스 : ", math.comb(deck_cnt-need_cnt,turn-need_cnt))

    TR_pr = round(TR_case / total_case * 100,4)
    print("트리플 확률은? : ",TR_pr,"%")
    Pbs.append(TR_pr)
    
    # 10.투페어 확률
    TP_pr = 0
    TP_case = 0

    for i in range(13): # 각 숫자별 원페어 될 확률 계산
        TP_mini_max=0
        TP_mini=0
        for j in range(13): # 각 숫자별 원페어 될 확률 계산 (i,j페어 확률계산)
            if(i==j):
                continue
            my_have_cnt1 = 0 # 내가가진 족보 필요 카드 수1
            need_cnt1 = 2    # 족보에 총 필요한 카드 수1
            my_have_cnt2 = 0 # 내가가진 족보 필요 카드 수2
            need_cnt2 = 2    # 족보에 총 필요한 카드 수2

            # 상대방이, 내가 필요한 카드를 3장이상 가지고 있으면 continue
            if(ST_other_cards[i] >= 3 or ST_other_cards[j] >= 3):
                continue

            # 내가 가진 카드가 족보에 해당하면 카운트
            my_have_cnt1 = ST_my_cards[i]
            my_have_cnt2 = ST_my_cards[j]
            need_cnt1 = 2 - my_have_cnt1
            need_cnt2 = 2 - my_have_cnt2

            complete_flag = 0
            if(need_cnt1 <= 0 and need_cnt2 <= 0):
                TP_case = total_case
                complete_flag = 1
                break
            
            if(need_cnt1 <= 0):
                need_cnt1 = 0
            if(need_cnt2 <= 0):
                need_cnt2 = 0


            # 남은턴보다 필요카드가 많다면, continue
            if(need_cnt1+need_cnt2 > turn): 
                continue
            TP_mini = math.comb(4-ST_my_cards[i]-ST_other_cards[i],need_cnt1) * math.comb(4-ST_my_cards[j]-ST_other_cards[j],need_cnt2) * math.comb(deck_cnt-need_cnt1-need_cnt2,turn-need_cnt1-need_cnt2)
            if(TP_mini_max < TP_mini):
                TP_mini_max = TP_mini
        if(complete_flag == 1):
            break
        #print(i+1,"투페어 확률 : ",TP_mini_max)
        TP_case += TP_mini_max
    
    TP_pr = round(TP_case / total_case * 100,4)
    print("투페어 확률은? : ",TP_pr,"%")
    Pbs.append(TP_pr)
    

    # 11.원페어 확률
    OP_pr = 0
    OP_case = 0

    for i in range(13): # 각 숫자별 원페어 될 확률 계산
        my_have_cnt = 0 # 내가가진 족보 필요 카드 수
        need_cnt = 2    # 족보에 총 필요한 카드 수        

        # 상대방이, 내가 필요한 카드를 3장이상 가지고 있으면 continue
        if(ST_other_cards[i] >= 3):
            continue

        # 내가 가진 카드가 족보에 해당하면 카운트
        my_have_cnt = ST_my_cards[i]
        need_cnt = 2 - my_have_cnt
        if(need_cnt <= 0):
            OP_case = total_case
            break
        
        # 남은턴보다 필요카드가 많다면, continue
        if(need_cnt > turn): 
            continue
        OP_case += math.comb(4-ST_my_cards[i]-ST_other_cards[i],need_cnt) * math.comb(deck_cnt-(4-ST_my_cards[i]-ST_other_cards[i]),turn-need_cnt)
        

    OP_pr = round(OP_case / total_case * 100,4)
    print("원페어 확률은? : ",OP_pr,"%")
    Pbs.append(OP_pr)

    return Pbs


def findPokerHand(hand):  #현재 패 확인 함수
    ranks = []
    suits = []
    possibleRanks = []

    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
        if rank == "A":
            rank = 14
        elif rank == "K":
            rank = 13
        elif rank == "Q":
            rank = 12
        elif rank == "J":
            rank = 11
        ranks.append(int(rank))
        suits.append(suit)

    sortedRanks = sorted(ranks)

    # Royal Flush and Straight Flush and Flush
    if suits.count(suits[0]) == 5: # Check for Flush
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks \
                and 10 in sortedRanks:
            possibleRanks.append(10)
        elif all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
            possibleRanks.append(9)
        else:
            possibleRanks.append(6) # -- Flush

    # Straight
    # 10 11 12 13 14
    #  11 == 10 + 1
    if all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
        possibleRanks.append(5)

    handUniqueVals = list(set(sortedRanks))

    # Four of a kind and Full House
    # 3 3 3 3 5   -- set --- 3 5 --- unique values = 2 --- Four of a kind
    # 3 3 3 5 5   -- set -- 3 5 ---- unique values = 2 --- Full house
    if len(handUniqueVals) == 2:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 4:  # --- Four of a kind
                possibleRanks.append(8)
            if sortedRanks.count(val) == 3:  # --- Full house
                possibleRanks.append(7)

    # Three of a Kind and Pair
    # 5 5 5 6 7 -- set -- 5 6 7 --- unique values = 3   -- three of a kind
    # 8 8 7 7 2 -- set -- 8 7 2 --- unique values = 3   -- two pair
    if len(handUniqueVals) == 3:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 3:  # -- three of a kind
                possibleRanks.append(4)
            if sortedRanks.count(val) == 2:  # -- two pair
                possibleRanks.append(3)

    # Pair
    # 5 5 3 6 7 -- set -- 5 3 6 7 - unique values = 4 -- Pair
    if len(handUniqueVals) == 4:
        possibleRanks.append(2)

    if not possibleRanks:
        possibleRanks.append(1)
    # print(possibleRanks)
    pokerHandRanks = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of a Kind", 7: "Full House", 6: "Flush",
                      5: "Straight", 4: "Three of a Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}
    output = pokerHandRanks[max(possibleRanks)]
    print(hand, output)
    return output


def listitem_touppercase(list):
    temp=[]
    for i in list:
        temp.append(i.upper())
    return temp


def findPokerHand2(hand,other_hand):  #현재 패 확인 함수_가공
    ranks = []
    suits = []
    possibleRanks = []



    # 0-1. 초기 처리
    Pbs=[] # 리턴할 리스트 (확률값들)
    deck =["AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
           "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
           "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",
           "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC"]
    
    for i in hand:
        deck.remove(i)
    for i in other_hand:
        deck.remove(i)

    my_cnt = len(hand) # 내가 가진 카드의 수
    turn = 7 - my_cnt # 남은 턴

    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
        if rank == "A":
            rank = 14
        elif rank == "K":
            rank = 13
        elif rank == "Q":
            rank = 12
        elif rank == "J":
            rank = 11
        ranks.append(int(rank))
        suits.append(suit)

    sortedRanks = sorted(ranks)

    for c4 in range(len(deck)):
        
        for c3 in range(len(deck)):
            if(c4 == c3):
                continue
            for c2 in range(len(deck)):
                if(c2 == c3 or c2 == c4):
                    continue
                for c1 in range(len(deck)):
                    if(c1 == c2 or c1 == c2 or c1 == c4):
                        continue




    # Royal Flush and Straight Flush and Flush
    if suits.count(suits[0]) == 5: # Check for Flush
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks \
                and 10 in sortedRanks:
            possibleRanks.append(10)
        elif all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
            possibleRanks.append(9)
        else:
            possibleRanks.append(6) # -- Flush

    # Straight
    # 10 11 12 13 14
    #  11 == 10 + 1
    if all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
        possibleRanks.append(5)

    handUniqueVals = list(set(sortedRanks))

    # Four of a kind and Full House
    # 3 3 3 3 5   -- set --- 3 5 --- unique values = 2 --- Four of a kind
    # 3 3 3 5 5   -- set -- 3 5 ---- unique values = 2 --- Full house
    if len(handUniqueVals) == 2:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 4:  # --- Four of a kind
                possibleRanks.append(8)
            if sortedRanks.count(val) == 3:  # --- Full house
                possibleRanks.append(7)

    # Three of a Kind and Pair
    # 5 5 5 6 7 -- set -- 5 6 7 --- unique values = 3   -- three of a kind
    # 8 8 7 7 2 -- set -- 8 7 2 --- unique values = 3   -- two pair
    if len(handUniqueVals) == 3:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 3:  # -- three of a kind
                possibleRanks.append(4)
            if sortedRanks.count(val) == 2:  # -- two pair
                possibleRanks.append(3)

    # Pair
    # 5 5 3 6 7 -- set -- 5 3 6 7 - unique values = 4 -- Pair
    if len(handUniqueVals) == 4:
        possibleRanks.append(2)

    if not possibleRanks:
        possibleRanks.append(1)
    # print(possibleRanks)
    pokerHandRanks = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of a Kind", 7: "Full House", 6: "Flush",
                      5: "Straight", 4: "Three of a Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}
    output = pokerHandRanks[max(possibleRanks)]
    print(hand, output)
    return output
















if __name__ == "__main__":
    '''
    #로티플 테스트
    print("======================")
    print("<<<<<로티플 테스트>>>>>")
    print("======================")
    madecalc(["KH", "AH", "QH", "JH", "10H"],["9C", "KD", "10C"]) # 이미 로티플
    madecalc(["KH", "QH", "JH", "10H", "8C"],["9C", "KD", "AH"]) # 상대방이 필요패 보유
    
    print("========3장 테스트=================")
    madecalc(["KH", "QH", "JH"],["8C"]) # 3장중 3장 완성
    madecalc(["KH", "QH", "JH", "10S"],["9C", "KD"]) # 4장중 3장 완성
    madecalc(["KH", "QH", "JH", "10S", "2S"],["9C", "KD", "10C"]) # 5장중 3장 완성
    madecalc(["KH", "QH", "JH", "10S", "2S", "3S"],["9C", "KD", "10C", "AD"]) # 6장중 3장 완성

    print("========4장 테스트=================")
    madecalc(["KH", "QH", "JH", "10H"],["9C", "KD"]) # 4장중 4장 완성
    madecalc(["KH", "QH", "JH", "10H", "10D"],["9C", "KD", "10C"]) # 5장중 4장 완성
    madecalc(["KH", "QH", "JH", "10H", "10D", "JD"],["9C", "KD", "10C", "AD"]) # 6장중 4장 완성
    
    #스티플 테스트
    print("======================")
    print("<<<<<스티플 테스트>>>>>")
    print("======================")
    madecalc(["4H", "5H", "6H"],["9C"]) # 3장중 3장 완성
    madecalc(["4H", "5H", "6H"],["2H"]) # 3장중 3장 완성, 상대가 하나 가지고 있음
    madecalc(["5H", "6H", "7H"],["9C"]) # 3장중 3장 완성
    madecalc(["5H", "6H", "7H"],["2H"]) # 3장중 3장 완성, 상대가 하나 가지고 있음
    madecalc(["5H", "6H", "7H"],["3H"]) # 3장중 3장 완성, 상대가 하나 가지고 있음
    madecalc(["4H", "6H", "8H"],["5S"]) # 3장중 3장 완성
    madecalc(["4H", "6H", "8H"],["5H"]) # 3장중 3장 완성, 상대가 하나 가지고 있음
    madecalc(["4H", "6H", "8H", "9H"],["7H", "5H"]) # 상대가 두개 가지고 있음
    madecalc(["4H", "6H", "8H", "9S"],["7H", "5H"]) # 상대가 두개 가지고 있음, 불가
    madecalc(["4H", "5H", "6H", "7H"],["9C", "KD"]) # 4장중 4장 완성
    madecalc(["4H", "5H", "6H", "7H", "8S",],["9C", "KD", "8C"]) # 5장중 4장 완성
    madecalc(["4H", "5H", "6H", "7H", "8S", "7S"],["9C", "KD", "8C","7C"]) # 6장중 4장 완성
    madecalc(["4H", "5H", "6H", "8H", "9H", "10H"],["9C", "KD", "8C","7C"]) # 6장중 4장 완성, 사이에 빈 값
    madecalc(["4H", "5H", "6H", "8H", "9H", "10H"],["9C", "KD", "8C","7H"]) # 6장중 4장 완성, 상대가 필요패 가지고 있음
    madecalc(["10H", "10S", "10C", ],["10D"]) # 완성된게없음, 4장 쭉 받아야됨
    madecalc(["4H", "5H", "6H", "7H", "8H" ],["10D","11D","12D"]) # 이미 완성
    
    print("======================")
    print("<<<<<포카드 테스트>>>>>")
    print("======================")
    madecalc(["AS", "AD", "AH"],["KS"]) # 3장완성
    madecalc(["AS", "AD", "AH"],["AC"]) # 3장완성, 상대방이 가지고있음
    madecalc(["AS", "AD", "AH"],["KS","QS","JS","10S"]) # 3장 중 3장완성, 5인게임, 상대방없음
    madecalc(["AS", "AD", "AH","KD"],["KS","QS","JS","10S","9S","8S","7S","6S"]) # 4장 중 3장완성, 5인게임, 상대방없음
    madecalc(["AS", "AD", "AH","KD", "QD"],["KS","QS","JS","10S","9S","8S","7S","6S","5S","4S","3S","2S"]) # 5장 중 3장완성, 5인게임, 상대방없음
    madecalc(["AS", "AD", "AH","KD", "QD", "JD"],["KS","QS","JS","10S","9S","8S","7S","6S","5S","4S","3S","2S","5H","4H","3H","2H"]) # 6장 중 3장완성, 5인게임, 상대방없음
    madecalc(["AS", "AD", "AH","KD", "QD", "AC"],["KS","QS","JS","10S","9S","8S","7S","6S","5S","4S","3S","2S","5H","4H","3H","2H"]) # 이미 완성
    madecalc(["KS", "KD", "KH","KC"],["QS","QD"]) # 이미 완성
    madecalc(["QS", "QD", "QH","QC"],["JS","JD"]) # 이미 완성
    print("======================")
    print("<<<<<플러쉬 테스트>>>>>")
    print("======================")
    
    
    madecalc(["5S", "3S", "6S", "KS", "JS"],["KD","QD","JD"]) # 이미 플러쉬 완성, 스페이드
    madecalc(["5C", "3C", "6C", "KC", "JC"],["KD","QD","JD"]) # 이미 플러쉬 완성, 클로버
    madecalc(["5C", "3C", "6C", "KC", "JC", "AS"],["KD","QD","JD"]) # 이미 플러쉬 완성, 클로버
    madecalc(["5S", "3S", "6S", "KS"],["AD", "2D"]) # 4장 중 4장완성, 상대방 없음
    madecalc(["5S", "3S", "6S", "KS"],["AS", "2S", "4S", "7S", "8S", "9S", "10S", "JS"]) # 4장 중 4장완성, 5인게임, 상대방이 하나빼고 다가짐
    madecalc(["5S", "3S", "6S", "KS", "QC"],["AS", "2S", "4S", "7S", "8S", "9S", "10S", "JS", "QS"]) # 4장 중 4장완성, 4인게임, 상대방이 다가짐
    madecalc(["5S", "3S", "6D", "KD"],["AS", "2D", "4H", "7C"]) # 4장 중 2장완성짜리 두개, 3인게임
    madecalc(["AS", "2S", "3S"],["5H"]) # 3장 중 3장 완성
    madecalc(["AS", "2S", "3S"],["5S"]) # 3장 중 3장 완성
    madecalc(["AS", "2S", "3S", "KS"],["5C", "8C"]) # 3장 중 3장 완성
    madecalc(["AS", "2S", "3S", "KS"],["5S", "8S"]) # 3장 중 3장 완성
    madecalc(["5S", "3S", "6S", "KS","AD","2D"],["8S", "9S", "10S", "JS"]) # 6장 중 4장완성, 2인게임
    madecalc(["5S", "3S", "6S", "KS","AD","2D"],["8D", "9D", "10D", "JD"]) # 6장 중 4장완성, 2인게임
    madecalc(["5S", "3S", "6S", "KS","KD","KH"],["AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H"]) # 6장 중 4장완성, 5인게임

    
    print("======================")
    print("<<<<<마운틴 테스트>>>>>")
    print("======================")
    madecalc(["KH", "AH", "QH", "JH", "10H"],["9C", "KD", "10C"]) # 이미 마운틴
    madecalc(["KS", "AD", "QH", "JC", "10S"],["9C", "KD", "10C"]) # 이미 마운틴
    madecalc(["KC", "AH", "QH", "JH", "10H"],["9C", "KD", "10C"]) # 이미 마운틴
    madecalc(["KS", "AD", "QH"],["9C"]) # 3장 중 3장 완성
    madecalc(["KH", "QH", "JH", "10H", "10D", "JD"],["9C", "KD", "10C", "AD"]) # 6장중 4장 완성
    madecalc(["KH", "QH", "JH", "10H", "10D", "JD"],["AS", "AD", "AH", "9D"]) # 6장중 4장 완성

    print("======================")
    print("<<<<<백스트레이트 테스트>>>>>")
    print("======================")
    madecalc(["AH", "5H", "2H", "3H", "4H"],["9C", "KD", "10C"]) # 이미 백스트레이트
    madecalc(["AS", "2D", "3H", "4C", "5S"],["9C", "KD", "10C"]) # 이미 백스트레이트
    madecalc(["AS", "4D", "5H"],["9C"]) # 3장 중 3장 완성
    madecalc(["AH", "2H", "3H", "4H", "10D", "JD"],["9C", "KD", "10C", "AD"]) # 6장중 4장 완성
    madecalc(["3H", "5D", "2H", "AH", "9D", "JD"],["AS", "AD", "AC", "9D"]) # 6장중 4장 완성

    print("======================")
    print("<<<<<스트레이트 테스트>>>>>")
    print("======================")
    madecalc(["KS", "QD", "JH", "10C", "AS"],["9C", "KD", "10D"]) # 5장 중 4장 완성
    madecalc(["6H", "5H", "2H", "3H", "4H"],["9C", "KD", "10C"]) # 이미 스트레이트
    
    madecalc(["4H", "5H", "6H", "7H", "8H" ],["10D","11D","12D"]) # 이미 스티플 완성
    madecalc(["KH", "9H", "QH", "JH", "10H"],["9C", "KD", "10C"]) # 이미 스티플 완성
    madecalc(["KS", "QD", "JH", "10C", "9S"],["9C", "KD", "10D"]) # 이미 스트레이트
    madecalc(["KS", "QD", "JH"],["10D"]) # 3장 중 3장 완성
    madecalc(["4S", "6D", "8H"],["AS"]) # 3장 중 3장 완성
    madecalc(["5S", "7D", "9H"],["AS"]) # 3장 중 3장 완성
    madecalc(["6S", "7D", "8H"],["AS"]) # 3장 중 3장 완성
    madecalc(["5S", "6D", "7H"],["AS"]) # 3장 중 3장 완성
    madecalc(["5S", "6D", "7H"],["2S"]) # 3장 중 3장 완성
    madecalc(["KS", "QD", "JH"],["AS"]) # 3장 중 3장 완성
    madecalc(["KS", "QD", "JH", "4H", "5S","3S"],["10D","9D","8D","7D"]) # 6장 중 3장 완성
    madecalc(["KS", "QD", "JH", "10H", "5S","3S"],["9S","9D","9H","9C"]) # 6장 중 4장 완성, 상대가 나머지 다 가지고있음
    

    print("======================")
    print("<<<<<페어, 트리플, 풀하우스 테스트>>>>>")
    print("======================")
    madecalc(["AS", "AD", "AC"],["AH"]) # 3장 중 3장 완성
    madecalc(["KS", "KD", "KC"],["AH"]) # 3장 중 3장 완성
    madecalc(["KS", "QD", "JH", "10C", "9S"],["9C", "KD", "10D"]) # 이미 스트레이트
    madecalc(["AS", "AD", "AC","KS", "KD", "KC"],["AH","2H","3H","4H"]) # 3장 중 3장 완성 X 2
    madecalc(["AS", "AD", "2C","2S", "3D", "3C"],["AH","2H","3H","4H"]) # 3장 중 2장 완성 X 3
    madecalc(["AS", "AD", "2C","2S"],["5H","5D","3H","4H"]) # 3장 중 2장 완성 X 2
    madecalc(["AS", "2S", "3S"],["5H"]) # 3장 중 2장 완성 X 2
    madecalc(["AS", "AD", "2C","2S", "3D", "3C"],["AH","2H","3H","4H"]) # 3장 중 2장 완성 X 3
    madecalc(["AS", "AC", "3S"],["5H"]) 
    madecalc(["AS", "AC", "AD"],["AH"]) 
    madecalc(["AS", "2S", "3S", "4S"],["KH","KD"])
    madecalc(["AS", "2S", "3S", "4S", "5S"],["KH","KD","KS"])
    '''
    print(madecalc(["6S", "2S", "3S", "4S", "5S"],["KH","KD","KS"]))



    

    
    

    


    

"""
    findPokerHand(["KH", "AH", "QH", "JH", "10H"])  # Royal Flush
    findPokerHand(["QC", "JC", "10C", "9C", "8C"])  # Straight Flush
    findPokerHand(["5C", "5S", "5H", "5D", "QH"])  # Four of a Kind
    findPokerHand(["2H", "2D", "2S", "10H", "10C"])  # Full House
    findPokerHand(["2D", "KD", "7D", "6D", "5D"])  # Flush
    findPokerHand(["JC", "10H", "9C", "8C", "7D"])  # Straight
    findPokerHand(["10H", "10C", "10D", "2D", "5S"])  # Three of a Kind
    findPokerHand(["KD", "KH", "5C", "5S", "6D"])  # Two Pair
    findPokerHand(["2D", "2S", "9C", "KD", "10C"])  # Pair
    findPokerHand(["KD", "5H", "2D", "10C", "JH"])  # High Card
"""