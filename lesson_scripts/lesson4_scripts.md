# Lesson 4: Refined, Alien Invasion Game Development

上次的课程我们完成了在游戏界面中添加外星人和外星人的战队、让外星人动起来和飞船射击子弹击落外星人，但是还差一点点这个游戏开发才能结束哦，比如它的速度好像僵尸非常不协调，它们有足够的提醒让用户如何开始游戏，它也没有记分系统，对了它甚至可以永远玩下去。接下来我们就要完成这些任务...

下图是我们之前的成功，在开始前我们先运行看一下吧，让我们处在同一起跑线。
![Lesson 3 Final Product](https://s2.loli.net/2022/06/10/1eglCM64IuiSAf2.gif)

## 今天我们要完成如下的目标：

- 让游戏可以结束
- 游戏介绍和操作说明
- 点击`开始(START)`进行游戏
- 增加分数系统


## 让游戏可以结束
要是一场游戏你始终都赢，那有什么意义呢？那在这个游戏中我们怎么定义游戏结束呢？如果玩家来不及将所有的外星人击落，那么外星人就会和飞船接触，当接触的时候它也就结束了；当外星人从飞船身边落下的时候（还没来得及消灭），也判定为玩家失败，但是可以给玩家增加机会；还有就是当玩家的所有机会都用完了，这个游戏也应该结束。现在让我们完成这些游戏结束的定义吧。

### 处理飞船和外星人的碰撞

>所在文件：`alien_invasion.py` <br/>
所在函数：`_update_aliens(self)`<br/>
所在行：`80`<br/>
```python
class AlienInvasion:

    def _update_aliens(self):
        """更新所有alien的位置信息"""
        self._check_fleet_edges()
        self.aliens.update()

        # //////////////////////////////////////////////////////////
        # 检测飞船和外星人的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('Ship hit!!!')
        # //////////////////////////////////////////////////////////
```
我们使用`spritecollideany`这个函数来检测两个2个对象是否发生接触（碰撞），这个函数接受两个参数，第一个参数是单独一个对象，第二个是一个组，它的功能是当组里面其中有一个对象与第一个对象发生碰撞是检测结果为真，后面的就不再进行检测，所以这个功能很好满足要求。现在我们放上一个`print`语句来测试发生碰撞的情况，现在你可以运行来看一下，当飞船和外星人发生碰撞时你的游戏后台就回输出：`Ship hit!!!`.

现在我们要处理当飞船和外星人接触时候，到底会发生什么？一般情况下我们会给玩家几次机会，而不是直接重新游戏，所以我们需要一个可以记录游戏状态的地方，你猜对了我们需要新建一个文件来完成所有操作。

请你在项目目录的下边创建一个叫：`game_stats.py`的文件吧，然后写入下面的信息。
>所在文件：`game_stats.py` <br/>
```python
class GameStats:
    """记录所有游戏状态信息"""
    def __init__(self, ai_game): 
        """初始化""" 
        self.settings = ai_game.settings 
        self.reset_stats()
    
    def reset_stats(self):
        """改变初始信息.""" 
        self.ships_left = self.settings.ship_limit
```

给飞船赋予初始的生命值。
>所在文件：`settings.py` <br/>
所在函数：`__init__(self)`<br/>
所在行：`13`<br/>
```python
class Settings:

    def __init__(self) -> None:
        """Initialize the game's settings"""
        # Ship settings
        self.ship_speed = 1.5
        # //////////////////////////////////////////////////////////
        self.ship_limit = 3
        # //////////////////////////////////////////////////////////
```

将 `GameStats`导入到`alien_invasion.py`中去
```python
import sys

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
# //////////////////////////////////////////////////////////
from game_stats import GameStats
# //////////////////////////////////////////////////////////
```
初始化`GameStats`对象。初始化的位置很重要哦，我们需要在游戏基本信息加载完成后再进行初始化，并且还要在其它发生前完成初始化，要不然这些信息不回发生左右。

>所在文件：`alien_invasion.py` <br/>
所在函数：`__init__(self)`<br/>
所在行：`20`<br/>
```python
class AlienInvasion:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)

        # //////////////////////////////////////////////////////////
        # Create an instance to store game statistics. 
        self.stats = GameStats(self)
        # //////////////////////////////////////////////////////////       
```

我们需要在每次发生碰撞的时候将飞船的生命值减少`1`，清空所有的alien和bullets集合，重新创建新的外星队伍，将飞居中。我们在`alien_invasion.py`里面通过建立一个新的函数来专门干这件事情，函数名叫做`_ship_hit()`。

>所在文件：`alien_invasion.py` <br/>
所在函数：`_ship_hit(self)`<br/>
```python
class AlienInvasion:
    
    # //////////////////////////////////////////////////////////
    def _ship_hit(self):
        # 生命值减少1
        self.stats.ships_left -= 1
        
        # 清空aliens和bullets
        self.aliens.empty()
        self.bullets.empty()

        # 创建新的fleet
        self._create_fleet()

        # 让飞船居中
        self.ship.center_ship()
        # 停一会儿重新开始
        sleep(0.5)    
    # //////////////////////////////////////////////////////////       
```
你会体会到我们之前将很多独立功能的代码写在一个函数里面的好处啦，我们只需要调用就可以了，不需要重新再去写那些逻辑，但是你也发现了我们需要重新来定义让飞船居中这件事情，即`center_ship()`这个函数我们还没写，快点来完成吧。
>所在文件：`ship.py` <br/>
所在函数：`center_ship(self)`<br/>
```python
class Ship:
    
    # //////////////////////////////////////////////////////////
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x) 
    # //////////////////////////////////////////////////////////       
```
最后我们将之前测试用的`print('Ship hit!!!')`替换成`_ship_hit()`就可以啦。
>所在文件：`alien_invasion.py` <br/>
所在函数：`_update_aliens(self)`<br/>
```python
class AlienInvasion:

    def _update_aliens(self):
        """更新所有alien的位置信息"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测飞船和外星人的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
        # //////////////////////////////////////////////////////////
            self._ship_hit()
        # //////////////////////////////////////////////////////////
```
**试一试**：运行代码看看吧，现在你能发现当任意一个外星人和飞船发生碰撞的时候，游戏会停止并且重新开始。对了当你在测试的时候，你要等外星人落下来，太费时间了，你可以调整一下参数哦。

### 外星人到达屏幕底部
如果外星人到达屏幕的底部我们也应该结束游戏才对，如何实现这件事情呢？我们来看一下。
我们现在`alien_invasion.py`文件里面增加一个函数来实现这个功能，首先获取屏幕的大小信息，通过一个循环来检测任意一个外星人的`alien.rect.bottom`超出`screen_rect.bottom`，如果为真则执行和上面飞船和外星人碰撞后一样事情`_ship_hit()`。

最后你还需要在`_update_aliens()`中调用`_check_aliens_bottom`这个函数。

>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_aliens_bottom(self)`和`_update_aliens()`<br/>
```python
class AlienInvasion:
    def _update_aliens(self):
        # ////////////////////上面的一致//////////////////////////
        self._check_aliens_bottom()
    
    # //////////////////////////////////////////////////////////
    def _check_aliens_bottom(self):
        """检查外星人是否到达屏幕的最底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    # //////////////////////////////////////////////////////////
```

### 让游戏结束
当我们的机会用完，即`ship_limit`等于`0`的时候，我们的游戏就该结束了，那么游戏结束应该是什么样子的呢？你想一想吧。其实很简单，游戏结束意味着你必须重新开始下一次游戏，即本次游戏完全结束是吧，实现这个功能很简单，我们来看一看。

我们先在`GameStats`中的`__init__()`方法里，设置一个状态变量`game_active`，并且让它一开始为`True`，当游戏结束的时候我们变回`False`后，整个游戏就不能玩了，也就结束了。

>所在文件：`game_stats.py` <br/>
所在函数：`__init__(self)`<br/>
```python
class GameStats:
    """记录所有游戏状态信息"""
    def __init__(self, ai_game): 
        """初始化""" 
        self.settings = ai_game.settings 
        self.reset_stats()

        # //////////////////////////////////////////////////////////
        self.game_active = True
        # //////////////////////////////////////////////////////////
```

然后我们需要在玩家用完所有的机会的时候让`game_active`的状态设置为`False`。

>所在文件：`alien_invasion.py` <br/>
所在函数：`_ship_hit(self)`<br/>
```python
class AlienInvasion:
    
    # //////////////////////////////////////////////////////////
    def _ship_hit(self):
        if self.stats.ship_left > 0:
            # 生命值减少1
            self.stats.ships_left -= 1
            
            # 清空aliens和bullets
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的fleet
            self._create_fleet()

            # 让飞船居中
            self.ship.center_ship()
            # 停一会儿重新开始
            sleep(0.5)    
        else:
            self.stats.game_active = False
    # //////////////////////////////////////////////////////////       
```

最后我们还要让我们的游戏正的停下来才行，所以我们需要甄别出当`game_active`为`True`的时候到底该运行那些指令呢，不错你想一下我们的游戏原理就会明白，我们只要在`game_active`为`True`的时候才对屏幕刷新，而当`game_active`为`False`的时候就不刷新了，也不去执行其它的内容了。

>所在文件：`alien_invasion.py` <br/>
所在函数：`run_game(self)`<br/>
```python
class AlienInvasion:
    
    def run_game(self):
        while True:
           self._check_event()
    # //////////////////////////////////////////////////////////
           if self.stats.game_active:
               self.ship.update()
               self._update_bullets()
               self._update_aliens()
    # //////////////////////////////////////////////////////////       
           self._update_screen()
```

好了，现在我们的游戏能够合乎逻辑的结束了，这样看起来它更像是一个完整的游戏啦，但是你会发现它还是和我们平时完的游戏有点区别，它还没有足够都的引导，接下来我们让它更加亲近玩家一点点吧。

## 游戏介绍和操作说明
你肯定有玩过游戏是吧？在你进入游戏的时候它都会给你一些提醒和说明，至少要知道这个是个什么游戏、它是怎么玩的等等的必要说明，有了这些信息，所有的玩家都知道该怎么操作啦，而我们的外星大战游戏现在就缺少这些东西，我们需要增加这些必要的说明，接下来我们先完成它。

几个常见的游戏界面示例：
![](https://s2.loli.net/2022/06/10/hWsUJuBDKzoEOFc.jpg)
![](https://s2.loli.net/2022/06/10/jzK4vbCpxHeq3rT.jpg)

我们先来设计一下我们的界面吧，我们尽量简单一点，不要太复杂的，你知道怎么弄就是了，在真正的游戏开发中，界面设计由美工部门花大量的时间来完成的。就像下面这个样子吧...

### 将游戏的说明指令放到界面上
![](https://s2.loli.net/2022/06/10/71lLUBeZmiuvz6x.jpg)

我们首先在项目文件目录下创建一个文件名叫做`game_info.py`来管理和游戏介绍信息相关的所有东西，到现在为止你应该感受到了为了让代码的复杂度降低我们尽量将有关系的代码写到一个文件里面，这样逻辑上要简单很多哦。

>所在文件：`game_info.py` <br/>
```python
import pygame

class GameInfo:
    def __init__(self, ai_game, msg) -> None:
        #1 //////////////////////////////////////////////////////////
        """Initialize GameInfo attributes."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Game instruction
        self.image = pygame.image.load('images/alien_invasion_start_scence.png')
        # //////////////////////////////////////////////////////////            
    
    # //////////////////////////////////////////////////////////            
    def blitme(self):
        self.screen.blit(self.image, (0,0))
    # //////////////////////////////////////////////////////////            
```
在这里我们创建了`GameInfo`这个对象来管理开始界面里的图像内容，在`#1`中我们对内容进行初始化。主要是将一张带有游戏说明的图片加载到游戏界面，这些内容前面都见过。

接着我们就把它放到游戏界面里去，通过修改`alien_invasion.py`里的`update_screen()`来实现。在这里要注意，我们在游戏开始的时候只是加载游戏说明的内容，不需要将飞船或者外星舰队加入到游戏中，所以我们做了流程控制，只有在游戏还没开始，即`game_active`为`False`的时候才开始出现说明。

>所在文件：`alien_invasion.py` <br/>
所在函数：`run_game(self)`<br/>
```python
class AlienInvasion:
    
def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        
        # ////////////////////////////////////////////////////////// 
        self.game_info.blitme()

        if self.stats.game_active:
            self.ship.blitme()


            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            # 将aliens显示在屏幕上
            self.aliens.draw(self.screen)
        # ////////////////////////////////////////////////////////// 
        
        # Must be the final to update the screen
        pygame.display.flip()
```
**试一试**：运行代码看看吧。
![](https://s2.loli.net/2022/06/10/8y3waPI4Kev12Fz.png)

### 增加一个开始的按钮
根据设计在我们的游戏开始界面的右侧有一个开始的按钮，这个按钮是有功能的，所以我们需要在pygame中将它绘制出来，要绘制这个按钮我们需要知道一些必要的信息，比如它的位置、大小、颜色等等，这些在设计的时候利用软件可以很容易地获取。
![](https://s2.loli.net/2022/06/10/t1F8MDmZsQfveNl.png)

首先我们对这个按钮的一些必要参数进行设定，在`game_info.py`这个文件里面，我们需要添加如下这些代码。
>所在文件：`game_info.py` <br/>
所在函数：`__init__(self)`<br/>
```python
class GameInfo:
    def __init__(self, ai_game, msg) -> None:
        #1 //////////////////////////////////////////////////////////
        # Set the dimensions and properties of the button.
        self.width, self.height = 360, 112
        self.button_color = (151, 195, 231)
        self.text_color = (32, 58, 102)
        self.font = pygame.font.SysFont(None, 80)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(653, 368, self.width, self.height)
        self._prep_msg(msg)        
        # //////////////////////////////////////////////////////////            
    
    #2 //////////////////////////////////////////////////////////
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    # //////////////////////////////////////////////////////////

    #3 //////////////////////////////////////////////////////////
    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    # //////////////////////////////////////////////////////////

    def blitme(self):
        self.screen.blit(self.image, (0,0))
        #4 //////////////////////////////////////////////////////////
        self.draw_button()
        # //////////////////////////////////////////////////////////  
```
在`#1`中我们用数值来描述了一个按钮的诸如：位置、大小、颜色、字体等信息
在`#2`中，因为pygame不能直接处理文字，所以必须使用一定的办法将文字信息转化成像素信息才能展示在游戏界面中，所以我们专门写了一个函数`_prep_msg(self, msg)`来生成可以显示在屏幕上的文本。
在`#3`中我们就用`fill`和`bilit`这两个函数将按钮绘制在屏幕上。
在`#4`中同时绘制游戏说明和按钮到屏幕上，这样我们在`alien_invasion.py`文件里绘制开始信息还是和原来一样不需要做任何的改变。

**试一试**：运行代码看看吧。
![](https://s2.loli.net/2022/06/10/DxaKFpUXcTeyfgZ.png)

现在我们的界面上已经有了一个按钮了，我们要让它有功能，就需要使用事件来控制，这样它就能侦听玩家的点击事件了。

>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_events(self)`<br/>
```python
class AlienInvasion:

    def _check_event(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #1 //////////////////////////////////////////////////////////
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # //////////////////////////////////////////////////////////
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    #2 //////////////////////////////////////////////////////////
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.game_info.rect.collidepoint(mouse_pos):
            self.stats.game_active = True
    # //////////////////////////////////////////////////////////
```
在`#1`中，pygame利用`MOUSEBUTTONDOWN`这个事件来侦听用户点击鼠标的事件，为了精确控制事件的响应我们需要`pygame.mouse.get_pos()`来获取鼠标的x和y坐标，然后我们把获取的信息传递给`#2`的`_check_play_button`函数，让它来处理鼠标的撞击`collidepoint`，当与我们的按钮矩形框碰撞时，我们就开始游戏啦。

**试一试**：运行代码看看吧。

到了这一步，你就可以玩你的游戏了，但是你会发现，游戏说明也还在，按钮也还在！而且超级乱！！看来还需要一些处理才可以哦。

我们需要修改一下`update_screen()`里面的逻辑，才能更好的展示内容，并且我们还要在按钮点击后把按钮的状态变为不可点击，还有如果你只是运行一次的话可能没有问题，但是当你多次运行的时候，你会发现游戏不可进行了，所以在点击开始按钮的时候还要对所有的东西进行重置，最后在游戏开始以后再把鼠标给隐藏了，在游戏结束后在让其显示。

>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_play_button(self)`<br/>
```python
class AlienInvasion:
    # //////////////////////////////////////////////////////////
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.game_info.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标
            pygame.mouse.set_visible(False)
    # //////////////////////////////////////////////////////////

    # //////////////////////////////////////////////////////////
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        if not self.stats.game_active:
            self.game_info.blitme()

        else:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # 将aliens显示在屏幕上
            self.aliens.draw(self.screen)
        
        # Must be the final to update the screen
        pygame.display.flip()
    # //////////////////////////////////////////////////////////

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # 生命值减少1
            self.stats.ships_left -= 1
            
            # 清空aliens和bullets
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的fleet
            self._create_fleet()

            # 让飞船居中
            self.ship.center_ship()

            # 停一会儿重新开始
            sleep(0.5)
        else:
            self.stats.game_active = False
            # //////////////////////////////////////////////////////////
            pygame.mouse.set_visible(True)
            # //////////////////////////////////////////////////////////
```

## 分数系统
我们的游戏界面还没有显示每次得了多少分，所以我们现在来完成显示分数。

### 在`GameStats`添加一个分数变量

>所在文件：`game_stats.py` <br/>
所在函数：`reset_stats(self)`<br/>
```python
class GameStats:
    
    def reset_stats(self):
        """改变初始信息.""" 
        self.ships_left = self.settings.ship_limit
        # //////////////////////////////////////////////////////////
        self.score = 0
        # //////////////////////////////////////////////////////////
```

### 显示分数
我们需要先创建一个分数对象，在项目目录下新建一个文件`scoreboard.py`来处理和分数相关的内容。这里主要使用pygame提供的字体处理模块来实现，其实我们在添加按钮的时候已经用过了，这里时一样的哦，我们加快速度吧。

>所在文件：`scoreboard.py` <br/>
```python
import pygame.font

class Scoreboard:
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.screen = ai_game.screen 
        self.screen_rect = self.screen.get_rect() 
        self.settings = ai_game.settings 
        self.stats = ai_game.stats
    
        # 字体信息基础设置.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 渲染分数的图像
        self.prep_score()
    

    def prep_score(self):
        """将字体转化成可以显示的图片."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,self.text_color, self.settings.bg_color)
        # 将分数信息显示在屏幕的右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """绘制到主界面."""
        self.screen.blit(self.score_image, self.score_rect)

```

### 将`Scoreboard`对象加入到主程序里

>所在文件：`alien_invasion.py` <br/>
所在函数：`__init__(self)`和`_update_screen(self)`<br/>
```python
# //////////////////////////////////////////////////////////
from scoreboard import Scoreboard
# //////////////////////////////////////////////////////////

class AlienInvasion:
    def __init__(self) -> None:
        
        self.stats = GameStats(self)
        
        # //////////////////////////////////////////////////////////
        self.sb = Scoreboard(self)
        # //////////////////////////////////////////////////////////
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        if not self.stats.game_active:
            self.game_info.blitme()

        else:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # 将aliens显示在屏幕上
            self.aliens.draw(self.screen)
            # //////////////////////////////////////////////////////////
            self.sb.show_score()
            # //////////////////////////////////////////////////////////
        
        # Must be the final to update the screen
        pygame.display.flip()
```
### 当击落外星人的时候把分数增加
>所在文件：`Settings.py` <br/>
所在函数：`__init__(self)`<br/>
```python

class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # 舰队运动方向，1代表向右，-1代表向左
        self.fleet_direction = 1

        # //////////////////////////////////////////////////////////
        self.alien_points = 50
        # //////////////////////////////////////////////////////////
```


>所在文件：`alien_invasion.py` <br/>
所在函数：`__init__(self)`<br/>
```python

class AlienInvasion:
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        # //////////////////////////////////////////////////////////
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
        # //////////////////////////////////////////////////////////
```

### 重置分数
>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_play_button(self)`<br/>
```python

class AlienInvasion:
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.game_info.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置
            self.stats.reset_stats()
            self.stats.game_active = True
            # //////////////////////////////////////////////////////////
            self.sb.prep_score()
            # //////////////////////////////////////////////////////////
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标
            pygame.mouse.set_visible(False)
        
```

## 自我提升：游戏升级

### 修改速度
>所在文件：`settings.py` <br/>
所在函数：`__init__(self)`<br/>
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        
        # //////////////////////////////////////////////////////////
        # 升级的时候难度提升系数
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        # //////////////////////////////////////////////////////////
    
    # //////////////////////////////////////////////////////////
    # 注意这里有些语句我们在前文定义过，这里把因为难度提升需要更改的参数放在一起
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
    # //////////////////////////////////////////////////////////
```
你可以参考修改后的`Settings`对象的代码。
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        self.caption = "Alien Invasion - Lesson 2"
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        # self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings 子弹相关的设定
        # self.bullet_speed = 2.0 # 子弹的速度
        self.bullet_width = 3 # 子弹的宽度
        self.bullet_height = 15 # 子弹的高度
        self.bullet_color = (60, 60, 60) # 子弹的颜色
        self.bullets_allowed = 3

        # Alien settings
        # self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # 舰队运动方向，1代表向右，-1代表向左
        # self.fleet_direction = 1

        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # 舰队运动方向，1代表向右，-1代表向左
        self.fleet_direction = 1
```

### 增加速度
>所在文件：`settings.py` <br/>
所在函数：`increase_speed(self)`<br/>
```python
class Settings:
    """A class to store all settings for Alien Invasion"""
    # //////////////////////////////////////////////////////////
    def increase_speed(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
    # //////////////////////////////////////////////////////////
```

重构`_update_bullets`，将碰撞独立出来，写一个新的函数`_check_bullet_alien_collisions`

>所在文件：`alien_invasion.py` <br/>
所在函数：`_update_bullets`和`_check_bullet_alien_collisions(self)`<br/>
```python
class AlienInvasion:
    """A class to store all settings for Alien Invasion"""
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        # //////////////////////////////////////////////////////////
        self._check_bullet_alien_collisions()
        # //////////////////////////////////////////////////////////
    
    # //////////////////////////////////////////////////////////
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    # //////////////////////////////////////////////////////////

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.game_info.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置
            # //////////////////////////////////////////////////////////
            self.settings.initialize_dynamic_settings()
            # //////////////////////////////////////////////////////////
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标
            pygame.mouse.set_visible(False)
```

### 解决有时候一箭双雕的时候不记分

>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_bullet_alien_collisions`<br/>
```python
class AlienInvasion:
    """A class to store all settings for Alien Invasion"""
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            # //////////////////////////////////////////////////////////
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            # //////////////////////////////////////////////////////////
            self.sb.prep_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
```

### 随着难度增加，如何增加分值呢
>所在文件：`settings.py` <br/>
所在函数：`increase_speed`<br/>
```python
class Settings:
    def __init__(self) -> None:
        """Initialize the game's settings"""
        # //////////////////////////////////////////////////////////
        self.score_scale = 1.5
        # //////////////////////////////////////////////////////////

    def increase_speed(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # //////////////////////////////////////////////////////////
        self.alien_points = int(self.alien_points * self.score_scale)
        # //////////////////////////////////////////////////////////
```

### 统计最高分
>所在文件：`game_stats.py` <br/>
所在函数：`__init__`<br/>
```python
class GameStats:
    """记录所有游戏状态信息"""
    def __init__(self) -> None:
        """Initialize the game's settings"""
        # //////////////////////////////////////////////////////////
        # 最高分
        self.high_score = 0
        # //////////////////////////////////////////////////////////

```
>所在文件：`scoreboard.py` <br/>
所在函数：`__init__`, `prep_high_score`,`check_high_score`, `show_score` <br/>
```python
class Scoreboard:
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""

        # Prepare the initial score
        self.prep_score()

        # //////////////////////////////////////////////////////////
        self.prep_high_score()
        # //////////////////////////////////////////////////////////


    # //////////////////////////////////////////////////////////
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    # //////////////////////////////////////////////////////////

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        # //////////////////////////////////////////////////////////
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # //////////////////////////////////////////////////////////
    
    # //////////////////////////////////////////////////////////
    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    # //////////////////////////////////////////////////////////

```

>所在文件：`alien_invasion.py` <br/>
所在函数：`__init__`<br/>
```python
class AlienInvasion:
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            # //////////////////////////////////////////////////////////
            self.sb.check_high_score()
            # //////////////////////////////////////////////////////////
    
```

### 显示游戏等级
>所在文件：`game_stats.py` <br/>
所在函数：`reset_stats()`<br/>
```python
class GameStats:
    """记录所有游戏状态信息"""
    
    def reset_stats(self):
        """改变初始信息.""" 
        self.ships_left = self.settings.ship_limit
        self.score = 0
        # //////////////////////////////////////////////////////////
        self.level = 1
        # //////////////////////////////////////////////////////////
```

>所在文件：`scoreboard.py` <br/>
所在函数：`__init__`, `prep_high_score`,`check_high_score`, `show_score` <br/>
```python
class Scoreboard:
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""

        # Prepare the initial score
        self.prep_score()
        self.prep_high_score()

        # //////////////////////////////////////////////////////////
        self.prep_level()
        # //////////////////////////////////////////////////////////


    # //////////////////////////////////////////////////////////
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,self.text_color, self.settings.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    # //////////////////////////////////////////////////////////

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # //////////////////////////////////////////////////////////
        self.screen.blit(self.level_image, self.level_rect)
        # //////////////////////////////////////////////////////////
```

>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_bullet_alien_collisions`<br/>
```python
class AlienInvasion:
    """A class to store all settings for Alien Invasion"""
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # //////////////////////////////////////////////////////////
            self.stats.level += 1
            self.sb.prep_level()
            # //////////////////////////////////////////////////////////

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.game_info.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            
            self.sb.prep_score()
            # //////////////////////////////////////////////////////////
            self.sb.prep_level()
            # //////////////////////////////////////////////////////////
            
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标
            pygame.mouse.set_visible(False)
```

### 显示剩下的机会
先让`Ship`对象继承`Sprite`，这样我们就能以组来控制他们了。

>所在文件：`ship.py` <br/>
所在函数：`_check_bullet_alien_collisions`<br/>
```python
import pygame
# //////////////////////////////////////////////////////////
from pygame.sprite import Sprite
# //////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////
class Ship(Sprite):
# //////////////////////////////////////////////////////////
    """A class to manage the ship"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting postion"""
        # //////////////////////////////////////////////////////////
        super().__init__()
        # //////////////////////////////////////////////////////////    
```

>所在文件：`scoreboard.py` <br/>
所在函数：``<br/>
```python
import pygame.font
# //////////////////////////////////////////////////////////
from pygame.sprite import Group
from ship import Ship
# //////////////////////////////////////////////////////////

class Scoreboard:
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        # //////////////////////////////////////////////////////////
        self.ai_game = ai_game
        # //////////////////////////////////////////////////////////
        self.screen = ai_game.screen 
        self.screen_rect = self.screen.get_rect() 
        self.settings = ai_game.settings 
        self.stats = ai_game.stats
    
        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare the initial score
        self.prep_score()

        self.prep_high_score()

        self.prep_level()
        # //////////////////////////////////////////////////////////
        self.prep_ships()
        # //////////////////////////////////////////////////////////

    # //////////////////////////////////////////////////////////
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    # //////////////////////////////////////////////////////////

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # //////////////////////////////////////////////////////////
        self.ships.draw(self.screen)
        # //////////////////////////////////////////////////////////
```
>所在文件：`alien_invasion.py` <br/>
所在函数：`_check_bullet_alien_collisions`<br/>
```python
class AlienInvasion:
    """A class to store all settings for Alien Invasion"""

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.game_info.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            
            self.sb.prep_score()
            self.sb.prep_level()
            # //////////////////////////////////////////////////////////
            self.sb.prep_ships()
            # //////////////////////////////////////////////////////////

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # 生命值减少1
            self.stats.ships_left -= 1
            # //////////////////////////////////////////////////////////
            self.sb.prep_ships()
            # //////////////////////////////////////////////////////////
```