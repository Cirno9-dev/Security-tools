# DicCreator

```
     _______  __           ______                               __                       
    /       \/  |         /      \                             /  |                      
    $$$$$$$  $$/  _______/$$$$$$  | ______   ______   ______  _$$ |_    ______   ______  
    $$ |  $$ /  |/       $$ |  $$/ /      \ /      \ /      \/ $$   |  /      \ /      \ 
    $$ |  $$ $$ /$$$$$$$/$$ |     /$$$$$$  /$$$$$$  |$$$$$$  $$$$$$/  /$$$$$$  /$$$$$$  |
    $$ |  $$ $$ $$ |     $$ |   __$$ |  $$/$$    $$ |/    $$ | $$ | __$$ |  $$ $$ |  $$/ 
    $$ |__$$ $$ $$ \_____$$ \__/  $$ |     $$$$$$$$//$$$$$$$ | $$ |/  $$ \__$$ $$ |      
    $$    $$/$$ $$       $$    $$/$$ |     $$       $$    $$ | $$  $$/$$    $$/$$ |      
    $$$$$$$/ $$/ $$$$$$$/ $$$$$$/ $$/       $$$$$$$/ $$$$$$$/   $$$$/  $$$$$$/ $$/       
                     __                       __                                      
                    /  |                     /  |                                       
                    $$ |____  __    __       $$ |    __ __    __                        
                    $$      \/  |  /  |      $$ |   /  /  \  /  |                       
                    $$$$$$$  $$ |  $$ |      $$ |   $$/$$  \/$$/                        
                    $$ |  $$ $$ |  $$ |      $$ |   /  |$$  $$<                         
                    $$ |__$$ $$ \__$$ |      $$ |   $$ |/$$$$  \                         
                    $$    $$/$$    $$ |      $$ |   $$ /$$/ $$  |                     
                    $$$$$$$/  $$$$$$$ |      $$__   $$ $$/   $$/                 
                             /  \__$$ |       /  \__$$ |                                
                            $$    $$/        $$    $$/                                 
                             $$$$$$/          $$$$$$/                              
```
A tool that can generate a dictionary.<br>
It use some keywords and date from your target ,top100 weak password ,and special symbols to generate a dictionary<br>
Also,you can only use the keywords date and special symbols to generate.<br>

## Usage

```shell
cd DicCreator
python DicCreator.py
```

## Example

```shell
python DicCreator.py -K 000322,ljx,github
```
**use keywords(000322,ljx,github),special symbols,and top100**
<br><br>

```shell
python DicCreator.py -D 2001:05:25 -K food
```
**use keywords(food),date(2001:05:25),special symbols,and top100**
<br><br>

```shell
python DicCreator.py -K ljx,github -N
```
**use keywords(ljx,github),special symbols**