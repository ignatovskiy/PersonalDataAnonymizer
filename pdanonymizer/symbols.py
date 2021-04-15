import os


start_symbol = """
::::    ::: :::::::::: :::::::::       :::     :::  :::::::       ::::::::  
:+:+:   :+: :+:        :+:    :+:      :+:     :+: :+:   :+:     :+:    :+: 
:+:+:+  +:+ +:+        +:+    +:+      +:+     +:+ +:+  :+:+            +:+ 
+#+ +:+ +#+ +#++:++#   +#++:++#:       +#+     +:+ +#+ + +:+         +#++:  
+#+  +#+#+# +#+        +#+    +#+       +#+   +#+  +#+#  +#+            +#+ 
#+#   #+#+# #+#        #+#    #+#        #+#+#+#   #+#   #+# #+# #+#    #+# 
###    #### ########## ###    ###          ###      #######  ###  ########  
"""

train_symbol = """
::::::::::: :::::::::      :::     ::::::::::: ::::    ::: ::::::::::: ::::    :::  ::::::::  
    :+:     :+:    :+:   :+: :+:       :+:     :+:+:   :+:     :+:     :+:+:   :+: :+:    :+: 
    +:+     +:+    +:+  +:+   +:+      +:+     :+:+:+  +:+     +:+     :+:+:+  +:+ +:+        
    +#+     +#++:++#:  +#++:++#++:     +#+     +#+ +:+ +#+     +#+     +#+ +:+ +#+ :#:        
    +#+     +#+    +#+ +#+     +#+     +#+     +#+  +#+#+#     +#+     +#+  +#+#+# +#+   +#+# 
    #+#     #+#    #+# #+#     #+#     #+#     #+#   #+#+#     #+#     #+#   #+#+# #+#    #+# 
    ###     ###    ### ###     ### ########### ###    #### ########### ###    ####  ########  
"""

test_symbol = """
::::::::::: ::::::::::  ::::::::  ::::::::::: ::::::::::: ::::    :::  ::::::::  
    :+:     :+:        :+:    :+:     :+:         :+:     :+:+:   :+: :+:    :+: 
    +:+     +:+        +:+            +:+         +:+     :+:+:+  +:+ +:+        
    +#+     +#++:++#   +#++:++#++     +#+         +#+     +#+ +:+ +#+ :#:        
    +#+     +#+               +#+     +#+         +#+     +#+  +#+#+# +#+   +#+# 
    #+#     #+#        #+#    #+#     #+#         #+#     #+#   #+#+# #+#    #+# 
    ###     ##########  ########      ###     ########### ###    ####  ########
"""

main_menu = """
|***********************|
| Choose needed option: |
|***********************|

[1] - Train model (training, post-training)
[2] - Test model (testing, counting accuracy)
[0] - Exit
"""

train_menu = """
|***********************|
| Choose needed option: |
|***********************|

[1] - Train model (from scratch)
[2] - Post-Train existing model
[9] - Return to Main Menu
[0] - Exit
"""

test_menu = """
|***********************|
| Choose needed option: |
|***********************|

[1] - Test model by dataset
[2] - Test model in real-time (by CLI queries)
[9] - Return to Main Menu
[0] - Exit
"""

train_result_menu = """
|***********************|
| Choose needed option: |
|***********************|

[1] - Test model by dataset
[2] - Test model in real-time (by CLI queries)
[9] - Return to Main Menu
[0] - Exit
"""

test_result_menu = """
|***********************|
| Choose needed option: |
|***********************|

[9] - Return to Main Menu
[0] - Exit
"""

test_rtc = """
|***********************|
| Choose needed option: |
|***********************|

[ ] - Text any letters to test model
[9] - Return to Main Menu
[0] - Exit
"""


def show_test():
    os.system('clear')
    print(test_symbol)


def show_train():
    os.system('clear')
    print(train_symbol)


def show_main_menu():
    os.system('clear')
    print(start_symbol)
    print(main_menu)


def show_train_menu():
    show_train()
    print(train_menu)


def show_test_menu():
    show_test()
    print(test_menu)
