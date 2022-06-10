# Lesson 3: Alien Invasion Game Development

上次的课程我们已经在飞船大战实践编程中，我们完成了对飞船的操控以及让飞船射击子弹，但是这个游戏还远没有结束，它能射击子弹了也能自由地左右移动射击子弹，可是它却没有目标可以射击（它的敌人Alien），现在让我们继续吧。

下图是我们之前的成功，在开始前我们先运行看一下吧，让我们处在同一起跑线。
![Lesson 2 Final Product](https://s2.loli.net/2022/05/24/j4Kcq63H2aAyZ1l.gif)

## 今天我们要完成如下的目标：

- 把外星人（Alien）添加到游戏中
- 一个外星人太少了，我们让它成为一个舰队

## 把外星人（Alien）添加到游戏中
这里的外星人（Alien）对于我们的游戏来说不过就是一张图片，所以你想这肯定会非常简单，因为我们之前已经做过这样的事情了，把飞船放在我们的游戏中，但是这里会有一点点不一样，我们来看看吧？

现在我们来拆解一下在这个过程中我们要干什么吧？
1. 创建Alien的类来管理所有关于外星人属性和方法
2. 先将一个外星人的图片加载到游戏的左上角
3. 给外星人周围留出一些空间，不让它太靠近左边和上面

### 1. 创建`alien.py`文件来管理外星敌人
在项目的根目录下新建一个`alien.py`的文件，`alien.py`文件很大程度上和`ship.py`文件的功能类似，所以我们可以适当借助一下，然后做一些必要的修改让它适合Alien的一些特性，它大概它向下面这个样子哦，仔细的你会发现它有一些变化。
> 所在文件：`alien.py`
```python
import pygame
#0 导入Sprite模块，让Alien来继承
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to manage the alien"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting postion"""
        #1 初始化被继承的Sprite
        super().__init__()
        self.screen = ai_game.screen

        #2 加载alien图片，获取它的矩形框
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        #3 重新定义alien的(x,y)坐标，将alien定位到屏幕的左上角，这样可以左右两边添加一定的空间
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #4 存储alien的横坐标
        self.x = float(self.rect.x)

```
你发现没，这个`Alien`对象和`Ship`对象的逻辑非常相似，但是还是有几个地方需要给大家说明一下哦
- #0 这个地方我们导入Sprite对象，Sprite有很多很好的特性，并且它是pygame里面自带的，我们可以借助这个对象少写很多代码，它能够很好地管理`组`这个概念，因为我们不光要放一个Alien在屏幕上，我们要放一个舰队在屏幕上的，后面实际用到的时候还会进一步给阐明的；
- #1 通过`super().__init()`初始化继承对象`Sprite`
- #2 通过`pygame.image.load()`加载alien图片，并且获取它的矩形框的属性：高、宽、x和y坐标。
- #3 重新定义alien的(x,y)坐标，将alien定位到屏幕的左上角，这样可以左右两边添加一定的空间
- #4 因为后面我们要创建一个舰队，我们需要控制它在屏幕横轴的速度，那么我们先把他的横坐标保存起来，后面可能会用到。

你发现，这个`Alien`对象和`Ship`对象有点不同哦，它没有使用`self.screen.blit(self.image, self.rect)`这个方法把它加载到屏幕上，因为我们可以使用`pygame`的组概念来自动把它放在屏幕上。

> **学习提醒**：我们在解决复杂问题的时候，总是将复杂的问题分成几个小的问题然后一个一个的解决简单的小问题，最后我们解决了这个大问题。

### 2. 将Alien导入到游戏中
我们先引入之前定义的Alien对象

> 所在文件：`alien_invasion.py`
```python
import sys

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
# 导入Alien对象
from alien import Alien
```

紧接着通过`pygame.Sprite.Group()`创建一个aliens组，我们可是需要的是一个舰队哦！然后我们新建一个方法来组建我们的舰队。

> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------

        # 注意：改这里--------------------------------
        # Aliens group
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
    
    def _create_fleet(self):
        pass
        # 注意：改这里--------------------------------
```

我们来花点时间构造`_create_fleet(self)`这个函数。
> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _create_fleet(self):
        # 注意：改这里--------------------------------
        # 创建一个外星人并将这个外星人加入到aliens组里面去
        alien = Alien(self)
        self.aliens.add(alien)
        # 注意：改这里--------------------------------
```

最后，我们将alien显示出来，我们需要在`_update_screen()`方法里面将alien画出来。
> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _update_screen(self):
        #上面都一样------------------------------
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 注意：改这里--------------------------------
        # 将aliens显示在屏幕上
        self.aliens.draw(self.screen)
        # 注意：改这里--------------------------------
        # Must be the final to update the screen
        pygame.display.flip()
```
**试一试**：运行代码看看吧，现在你应该看到如下图所示的样子了哦。
![](https://s2.loli.net/2022/05/26/eVhqPc2f7OHXC8o.gif)


## 一个外星人太少了，我们让它成为一个舰队
在创建舰队之前，我们需要考虑舰队的规模，很简单就是确定每一排可以容纳多少个alien图片，每一列可以容纳多少个alien，确定了这些之后我们就可以创建舰队了哦

### 每一排能够容纳多少个alien图片
一开始，我们的屏幕上已经有一个alien了，它占用了一个位置，为了让每个alien之间不用挨着太近，我们还需要让每个alien之间还要有点距离。我们通过下面的方式来确定。

> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _create_fleet(self):
        #上面都一样------------------------------
        
        # 注意：改这里--------------------------------
        # 计算横向可以容纳多少个外星人 
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # 创建一排外星人
        for alien_number in range(number_aliens_x):
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)
        # 注意：改这里--------------------------------
```
### 添加行数
> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _create_fleet(self):
        # 创建一个外星人并将这个外星人加入到aliens组里面去
        alien = Alien(self)
        self.aliens.add(alien)
        
        # 注意：改这里--------------------------------
        # 计算横向可以容纳多少个外星人 
        # alien_width = alien.rect.width
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算纵向能容纳的外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        # 创建一排外星人
        # for alien_number in range(number_aliens_x):
        #     alien = Alien(self)
        #     alien.x = alien_width + 2 * alien_width * alien_number
        #     alien.rect.x = alien.x
        #     self.aliens.add(alien)
        # 创建整个舰队
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien = Alien(self)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
                self.aliens.add(alien)
        # 注意：改这里--------------------------------
```
**试一试**：运行代码看看吧，现在你应该看到如下图所示的样子了哦。

## 重构`_create_fleet()`方法
你发现了吗，我们的`_create_fleet()`方法越来越庞大，这就告诉我们我们应该对它进行整理重构了
> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _create_fleet(self):
        # 创建一个外星人并将这个外星人加入到aliens组里面去
        alien = Alien(self)
        self.aliens.add(alien)
        
        # 计算横向可以容纳多少个外星人 
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算纵向能容纳的外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_aliens(alien_number, row_number)
                

    def _create_aliens(self, alien_number, row_number):
        """Create aliens in x,y direction"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)
```

## 让舰队动起来
是时候将我们的舰队运转起来了，接下来我们再将舰队动起来，让它更好玩一点哦。
> 所在文件：`settings.py`
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        #上面都一样------------------------------
        # Alien settings
        self.alien_speed = 1.0
```

> 所在文件：`alien.py`
```python
class Alien(Sprite):
    """A class to manage the alien"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting postion"""
        #1 初始化被继承的Sprite
        super().__init__()
        self.screen = ai_game.screen
        #上面都一样------------------------------
        # 注意：改这里--------------------------------
        self.settings = ai_game.settings
        #下面都一样------------------------------
    
    # 注意：新增update方法--------------------------------
    def update(self) -> None:
        """把舰队向右边移动"""
        self.x += self.settings.alien_speed
        self.rect.x = self.x
    # 注意：新增update方法--------------------------------
```

> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def run_game(self):
        while True:
           self._check_event()
           self.ship.update()
           self._update_bullets()
           # +++++++++++++注意：新增++++++++++++++++++++
           self._update_aliens()
           # +++++++++++++注意：新增++++++++++++++++++++
           self._update_screen()
    
    # +++++++++++++注意：新增++++++++++++++++++++
    def _update_aliens(self):
        """更新所有alien的位置信息"""
        self.aliens.update()
    # +++++++++++++注意：新增++++++++++++++++++++
```
> 所在文件：`settings.py`
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        #上面都一样------------------------------
         # Alien settings
        self.alien_speed = 1.0
        # +++++++++++++注意：新增++++++++++++++++++++
        self.fleet_drop_speed = 10
        # 舰队运动方向，1代表向右，-1代表向左
        self.fleet_direction = 1
        # +++++++++++++注意：新增++++++++++++++++++++
```
### 检测舰队是否触碰界面边缘
> 所在文件：`alien.py`
```python
class Alien(Sprite):
    """A class to manage the alien"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting postion"""
        #1 初始化被继承的Sprite
        super().__init__()
        self.screen = ai_game.screen
        #上面都一样------------------------------
        # 注意：改这里--------------------------------
        self.settings = ai_game.settings
        #下面都一样------------------------------
    
    # 注意：新增check_edges方法--------------------------------
    def check_edges(self):
        """碰触边缘检测，当外星人的右边大于屏幕最右边或者小于最左边时候返回真"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    # 注意：新增check_edges方法--------------------------------

    def update(self) -> None:
        """把舰队向右边移动"""
        # 注意：修改--------------------------------
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        # 注意：修改--------------------------------
        self.rect.x = self.x
```
现在我们需要根据是否碰触界面边沿来改变舰队的移动方向，我们需要到`alien_invasion.py`里面去更改
> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
   
    def _update_aliens(self):
        """更新所有alien的位置信息"""
        # +++++++++++++注意：新增++++++++++++++++++++
        self._check_fleet_edges()
        # +++++++++++++注意：新增++++++++++++++++++++
        self.aliens.update()
    
    # +++++++++++++注意：新增++++++++++++++++++++
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    # +++++++++++++注意：新增++++++++++++++++++++

    # +++++++++++++注意：新增++++++++++++++++++++
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1
    # +++++++++++++注意：新增++++++++++++++++++++
```
**试一试**：运行代码看看吧，现在你应该看到如下图所示的样子了哦。

## 检测子弹和外星人的碰撞
我们可以想见，当子弹和外星人碰触的时候，因该让子弹和外星人都消失才对，在pygame中用`pygame.sprite.groupcollide()`来检测两个元素的碰触。

> 所在文件：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
   
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
```
**试一试**：运行代码看看吧，现在你应该能够将外星人击落了，巨大的成功！
![](https://s2.loli.net/2022/06/10/1eglCM64IuiSAf2.gif)