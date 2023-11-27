def print_tree(node, prefix=''):
    print(prefix + node['name'])
    for child in node.get('children', []):
        print_tree(child, prefix=prefix + "  |")


def build_decision_tree_1(A:list, B:list, p=0.5):
    EV = [A*p + B*p for A, B in zip(A, B)]

    task1_tree = {
        'name': f'Оптимальний варіант <{max(EV)}>',
        'children': [
            {'name': f'Створення великого виробництва <{EV[0]}>', 'children': [
                                                {'name': f'Сприятливий стан <{A[0]}>'},
                                                {'name': f'Несприятливий стан <{B[0]}>'}]},
            {'name': f'Створення малого підприємства <{EV[1]}>', 'children': [
                                                {'name': f'Сприятливий стан <{A[1]}>'},
                                                {'name': f'Несприятливий стан <{B[1]}>'}
            ]},
            {'name': f'Продаж патенту <{EV[2]}>', 'children': [
                                                {'name': f'Сприятливий стан <{A[2]}>'},
                                                {'name': f'Несприятливий стан <{B[2]}>'}]}
        ]
    }
    print('\nЗАВДАННЯ 1')
    print_tree(task1_tree)

def build_decision_tree_2(A:list, B:list, P11:float, P12:float, P21:float, P22:float, Q:int, p=0.5, p1=0.75, p2=0.25):
    EV = [A*p + B*p for A, B in zip(A, B)]
    EV_p1 = [P11*A+P21*B for A, B in zip(A, B)]
    EV_p2 = [P12*A+P22*B for A, B in zip(A, B)]

    task2_tree = {
        'name': f'Оптимальний варіант <{max(max(EV), p1*max(EV_p1)+p2*max(EV_p2)-Q)}>',  # Root node name
        'children': [
            {
                'name': f'Не проводити огляд <{max(EV)}>',
                'children': [
                    {'name': f'Створення великого виробництва <{EV[0]}>', 'children': [
                        {'name': f'Сприятливий стан <{A[0]}>'},
                        {'name': f'Несприятливий стан <{B[0]}>'}
                    ]},
                    {'name': f'Створення малого підприємства <{EV[1]}>', 'children': [
                        {'name': f'Сприятливий стан <{A[1]}>'},
                        {'name': f'Несприятливий стан <{B[1]}>'}
                    ]},
                    {'name': f'Продаж патенту <{EV[2]}>', 'children': [
                        {'name': f'Сприятливий стан <{A[2]}>'},
                        {'name': f'Несприятливий стан <{B[2]}>'}
                    ]}
                ]
            },
            {
                'name': f'Проводити огляд <{p1*max(EV_p1)+p2*max(EV_p2)-Q}>', 
                'children': [
                    {
                        'name': f'Сприятливий ({p1}) <{max(EV_p1)}>',
                        'children': [
                            {'name': f"Створення великого виробництва <{EV_p1[0]}>", 'children': [
                                {'name': f'Сприятливий стан <{A[0]}>'},
                                {'name': f'Несприятливий стан <{B[0]}>'}
                            ]},
                            {'name': f"Створення малого підприємства <{EV_p1[1]}>", 'children': [
                                {'name': f'Сприятливий стан <{A[1]}>'},
                                {'name': f'Несприятливий стан <{B[1]}>'}
                            ]},
                            {'name': f"Продаж патенту <{EV_p1[2]}>", 'children': [
                                {'name': f'Сприятливий стан <{A[2]}>'},
                                {'name': f'Несприятливий стан <{B[2]}>'}
                            ]}
                        ]
                    },
                    {
                        'name': f'Несприятливий ({p2}) <{max(EV_p2)}>',
                        'children': [
                            {'name': f"Створення великого виробництва <{EV_p2[0]}>", 'children': [
                                {'name': f'Сприятливий стан <{A[0]}>'},
                                {'name': f'Несприятливий стан <{B[0]}>'}
                            ]},
                            {'name': f"Створення малого підприємства <{EV_p2[1]}>", 'children': [
                                {'name': f'Сприятливий стан <{A[1]}>'},
                                {'name': f'Несприятливий стан <{B[1]}>'}
                            ]},
                            {'name': f"Продаж патенту <{EV_p2[2]}>", 'children': [
                                {'name': f'Сприятливий стан <{A[2]}>'},
                                {'name': f'Несприятливий стан <{B[2]}>'}
                            ]}
                        ]
                    }
                ]
            }
        ]
    }


    print('\nЗАВДАННЯ 2')
    print_tree(task2_tree)


def build_decision_tree_3(A_probs:list, B_probs:list, defect_rates:list, K:int, N:int, L:int):
    EV_A = [round(defect_rate * K * N / 100, 1) for defect_rate in defect_rates]
    EV_B = [round(defect_rate * K * N / 100 - L, 1) for defect_rate in defect_rates] 

    A = sum(EV_A[i]*A_probs[i] for i in range(len(A_probs)))
    B = sum(EV_B[i]*B_probs[i] for i in range(len(B_probs)))

    task3_tree = {
        'name': f'Оптимальний варіант <-{min(A, B)}>',
        'children': [
            {'name': f'Виробник А <-{A}>', 
            'children': [
                            {'name': f'Брак {defect_rates[0]}% ({A_probs[0]}) <-{EV_A[0]}>'},
                            {'name': f'Брак {defect_rates[1]}% ({A_probs[1]}) <-{EV_A[1]}>'},
                            {'name': f'Брак {defect_rates[2]}% ({A_probs[2]}) <-{EV_A[2]}>'},
                            {'name': f'Брак {defect_rates[3]}% ({A_probs[3]}) <-{EV_A[3]}>'},
                            {'name': f'Брак {defect_rates[4]}% ({A_probs[4]}) <-{EV_A[4]}>'},
                        ]
            },
            {'name': f'Виробник B <-{B}>', 
            'children': [
                            {'name': f'Брак {defect_rates[0]}% ({B_probs[0]}) <-{EV_B[0]}>'},
                            {'name': f'Брак {defect_rates[1]}% ({B_probs[1]}) <-{EV_B[1]}>'},
                            {'name': f'Брак {defect_rates[2]}% ({B_probs[2]}) <-{EV_B[2]}>'},
                            {'name': f'Брак {defect_rates[3]}% ({B_probs[3]}) <-{EV_B[3]}>'},
                            {'name': f'Брак {defect_rates[4]}% ({B_probs[4]}) <-{EV_B[4]}>'},
                        ]
            }
        ]
    }

    print('\nЗАВДАННЯ 3')
    print_tree(task3_tree)

build_decision_tree_1(A=[600000, 350000, 70000],
                      B=[-300000, -70000, 70000])

build_decision_tree_2(A=[600000, 350000, 70000],
                      B=[-300000, -70000, 70000],
                      P11 = 0.8,  
                      P12 = 0.2,  
                      P21 = 0.25,  
                      P22 = 0.75,
                      Q = 20000)

build_decision_tree_3(A_probs=[0.5, 0.3, 0.1, 0.1, 0.05], 
                      B_probs=[0.45, 0.25, 0.25, 0.1, 0.1], 
                      defect_rates=[1, 2, 3, 4, 5], 
                      K=150, 
                      N=10000, 
                      L=1100)