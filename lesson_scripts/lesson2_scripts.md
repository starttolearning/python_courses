# Lesson 2: Alien Invasion Game Development

上次的课程我们已经在飞船大战实践编程中，我们完成了项目的设置、文件的添加、基础的设置、添加了飞船以及让飞船动起来，但是这个游戏还远没有结束，现在让我们继续吧。

下图是我们之前的成功，在开始前我们先运行看一下吧，让我们处在同一起跑线。

![Game Display in lesson 1](https://s2.loli.net/2022/05/22/cKArMkLHYsmuQd9.png "第一课中我们的成果")

## 今天我们要完成如下的目标：

- 重构`_check_events()`和`_update_screen`这两个方法
- 侦听按键事件，让飞船动起来
- 让飞船射击子弹

## 重构`_check_events()`和`_update_screen()`这两个方法

随着代码的增加，你会发现项目越来越乱了，任由发展会让你的项目无法控制。代码重构会很大程度上解决你的问题，而且会让你的代码看上去更加有逻辑性，从而可以增加代码的复用性。

我们先来看如何重构`_check_events()`吧，我们将管理事件（event）的程序写在一起，这样就会简化`run_game()`这个函数，也会让代码更加独立，做自己擅长的事情。

不过在我们进行修改之前，我们先来看一下效果吧。

> 修改的文件名称：`alien_invasion.py`

```python
class AlienInvasion:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    
    def run_game(self):
        while True:
    # 注意：这是之前的样子--------------------------------
            """Respond to keypress and mouse events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            """Update images on the screen, and flip to the new screen."""
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # Must be the final to update the screen（这里必须写在循环的最后一行执行，很重要）
            pygame.display.flip()
    # 注意：这是之前的样子--------------------------------

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
```
### 重构`_check_events()`
> 修改的文件名称：`alien_invasion.py`

```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def run_game(self):
        while True:
            # 注意：改这里--------------------------------
            self._check_events()
            # 注意：改上面--------------------------------
            """Update images on the screen, and flip to the new screen."""
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # Must be the final to update the screen（这里必须写在循环的最后一行执行，很重要）
            pygame.display.flip()

    # 注意这里添加_check_events ------------------
    def _check_events(self):
    """Respond to keypress and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
```
### 重构`_update_screen()`
我们继续重构`_update_screen()`，还是使用和`_check_events()`一样的方法。

> 修改的文件名称：`alien_invasion.py`

```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def run_game(self):
        while True:
    # 注意：改这里--------------------------------
            self._check_events()
            self._update_screen()
    # 注意：改上面--------------------------------

    # 注意这里添加_check_events ------------------
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Must be the final to update the screen
        pygame.display.flip()
```

好了，现在你再回去看看`run_game()`你会发现，它现在非常的干净，我们后面还会多次使用这样的方法来重构我们的代码。

**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

## 侦听按键事件，让飞船动起来
现在，我们就给我们的游戏玩家一些操作能力让飞船可以动起来吧，我们通过让玩家按动键盘上的左右键来实现对飞船的操作，我们先来让飞船向右边移动，然后我们使用同样的方法让它向左边移动，你将学会如何移动pygame里面的图片来实现对游戏中元素的操作和控制。

### 侦听`KEYDOWN`事件
我们首先要让这个游戏对我们的按键操作有反应。当玩家按下键盘上的一个按钮的时候，pygame把它当成一个事件（event），每个事件都可以通过`pygame.event.get()`方法来获取，还记得我们写的`_check_events()`方法吗，我们把它放在这里。每一次按键，对于pygame来说就会当成`KEYDOWN`事件哦。我们来看一下代码吧：

> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # 注意：改这里--------------------------------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 让飞船往右边移动
                    self.ship.rect.x += 1
        # 注意：改这里--------------------------------
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

现在当你按一按右键的时候，你会发现飞船往右边移动了一个像素，而且你还会发现它一动起来飞船不丝滑，如果这游戏就是这样，我敢说你会说：“真垃圾”，别急我们只需一点点改动就解决问题了，我们让它持续的移动就可以了。

先来看一下`ship.py`之前的样子吧。
```python
import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting postion"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ships.bmp')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
```

### 让飞船持续的移动
我们紧接着在`ship.py`里面添加下面的代码：

> 修改的文件名称：`ship.py`
```python
class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game) -> None:
        #上面都一样------------------------------
        
        # 注意：改这里--------------------------------
        # Movement flags
        self.moving_right = False
        # 注意：改这里--------------------------------
    
    # 注意：改这里--------------------------------
    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right:
            self.rect.x += 1
    # 注意：改这里--------------------------------
```

然后我们改事件：
> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 注意：改这里--------------------------------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 让飞船往右边移动
                    self.ship.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
            # 注意：改这里--------------------------------
```

最后我们，还要实时对ship在屏幕上进行更新操作：

> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    def run_game(self):
        while True:
            self._check_events()
            # 注意：改这里--------------------------------
            self.ship.update()
            # 注意：改这里--------------------------------
            self._update_screen()    
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

### 让飞船向左边移动吧

好了，我们把这种思路应用到左边的移动就大功告成了。

在`ship.py`里，做如下改动：
> 修改的文件名称：`ship.py`
```python
class Ship:

    def __init__(self, ai_game) -> None:
        #上面都一样------------------------------
        # Movement flags
        self.moving_right = False
        # 注意：改这里--------------------------------
        self.moving_left = False
        # 注意：改这里--------------------------------
    
    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_righ:
            self.rect.x += 1
        # 注意：改这里--------------------------------
        if self.moving_left:
            self.rect.x -= 1
        # 注意：改这里--------------------------------
```

在`alien_invasion.py`中做修改。
> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 注意：改这里--------------------------------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 让飞船往右边移动
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
            # 注意：改这里--------------------------------
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

### 调整飞船的移动速度

如何调整飞船的移动速度呢？
在`settings.py`中做修改。

> 修改的文件名称：`settings.py`
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        #上面都一样------------------------------

        # 注意：改这里--------------------------------
        # Ship settings
        self.ship_speed = 1.5
        # 注意：改这里--------------------------------
```
在`ship.py`里，做如下改动：
> 修改的文件名称：`ship.py`
```python
class Ship:

    def __init__(self, ai_game) -> None:
        #上面都一样------------------------------
        # Movement flags
        self.moving_right = False
        # 注意：改这里--------------------------------
        self.moving_left = False
        # 注意：改这里--------------------------------
    
    def update(self):
        """Update the ship's position based on movement flags."""
        # 注意：改这里--------------------------------
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        # 注意：改这里--------------------------------
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

### Bug Fixs Section

1. 你在飞船移动过程中，又一个小问题不知道你注意到没有？就是我们的飞船移动过程中还是缺少一点点丝滑感觉，有时候你不能刚好移动到界面的最右端和最左边，甚至有时候不是正居中，但是这种细节差距很小，你可能没注意到，但是值得我们去更改。

> 修改的文件名称：`ship.py`
```python
class Ship:

    def __init__(self, ai_game) -> None:
        #上面都一样------------------------------
        # 注意：改这里--------------------------------
        self.x = float(self.rect.x)  
        # 注意：改这里--------------------------------
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on movement flags."""
        # 注意：改这里--------------------------------
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x
        # 注意：改这里--------------------------------
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

2. 在开始之前请你试一下：一直按住键盘的左键或者右键，看一下效果吧。你发现没，当你在移动飞船的时候，你是不是可以将飞船移除你的视线外呀？这其实是一个bug，但是我们可以快速地解决它，来看一下。
在`ship.py`里，做如下改动：
```python

class Ship:
    def __init__(self, ai_game):
        #上面都一样------------------------------
    
    # 改这里
    def update(self):
        """Update the ship's position based on movement flags."""
        # 注意：改这里--------------------------------
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 注意：改这里--------------------------------
        self.rect.x = self.x
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

## 让飞船射击子弹

先来定义一下我们的子弹属性吧：
在`settings.py`里，做如下改动：
> 修改的文件名称：`settings.py`
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        #上面都一样------------------------------

        # 注意：改这里--------------------------------
        # Bullet settings 子弹相关的设定
        self.bullet_speed = 2.0 # 子弹的速度
        self.bullet_width = 3 # 子弹的宽度
        self.bullet_height = 15 # 子弹的高度
        self.bullet_color = (60, 60, 60) # 子弹的颜色
        # 注意：改这里--------------------------------
```

### 添加一个文件`bullet.py`
```python
import pygame

# 这里导入Sprite，因为我们的Bullte对象需要继承它
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game) -> None:
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0) and then set correct position
        # 使用Rect创建一个在（0，0）的一个元素，作为子弹
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
```
### 把子弹加入游戏中

将`bullets`存入一个组（Group）中
在`alien_invasion.py`里，做如下改动：
> 修改的文件名称：`alien_invasion.py`
```python
#上面都一样------------------------------
# 注意：改这里--------------------------------
# 导入Bullet类
from bullet import Bullet
# 注意：改这里--------------------------------

class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
        # Bullets group
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            # 注意：改这里--------------------------------
            self._update_bullets()
            # 注意：改这里--------------------------------
            self._update_screen()
    
    # 注意：改这里--------------------------------
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
    # 注意：改这里--------------------------------
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

### 射击出子弹

我们想一下，如果你要射击子弹你会做哪些操作呢？首先我们需要触发事件，那我们这里使用空格（SPACE）来触发事件，你应该还记得我们管理事件的地方在`_check_events()`方法里面对不对？所以我们首先要在它的最后面添加另外一个事件，请看下面的代码吧。然后我们是不是还要新增一个真正让子弹出现在屏幕上的方法，我们给它取名字叫`_fire_bullet()`。最后我们还需要对屏幕上的所有元素进行更新，这样它才会出现在界面里。

在`alien_invasion.py`里，做如下改动：

> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            #上面都一样------------------------------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 让飞船往右边移动
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            # 注意：改这里--------------------------------
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            # 注意：改这里--------------------------------
    
    # 注意：改这里--------------------------------
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
    # 注意：改这里--------------------------------

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # 注意：改这里--------------------------------
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 注意：改这里--------------------------------
        
        # Must be the final to update the screen
        pygame.display.flip()
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

### 删除旧的子弹
如果我们的子弹射出后一直都存在（这个时候你可能看不到它，因为它的坐标已经在我们的游戏界面外面了，但是事实上它还是在那里的），随着我们射击的子弹越来越多，管理子弹所需要的计算机资源就会增加，这显然会增加计算机的负担，那我们有必要对已经在界面外的子弹进行处理，让它们及时销毁。

在`alien_invasion.py`里，做如下改动：
> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        
        # 注意：改这里--------------------------------
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 注意：改这里-------------------------------- 
```

### 限制每次能够射击的子弹数量

如果你在游戏中可以无限的射击出子弹，我想这应该算作弊吧，而且对于计算机的性能来说负担也比较大。所以我们对每次能够射击的子弹进行限制一下可能会比较好。

在`settings.py`里，做如下改动：
> 修改的文件名称：`settings.py`
```python
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        #上面都一样------------------------------
        
        # Bullet settings 子弹相关的设定
        self.bullet_speed = 2.0 # 子弹的速度
        self.bullet_width = 3 # 子弹的宽度
        self.bullet_height = 15 # 子弹的高度
        self.bullet_color = (60, 60, 60) # 子弹的颜色
        # 注意：改这里--------------------------------
        self.bullets_allowed = 3
        # 注意：改这里--------------------------------
```
然后我们再对`alien_invasion.py`做如下改动：

```python
class AlienInvasion:
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        # Limiting the number of bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
```
**试一试**：运行代码看看吧，如果无法运行你可能需要花点时间找出为什么并改正它。

最后做一些重构和代码的bug调试吧。

## 重构`_check_keyup_events()`和`_check_keydown_events()`这两个方法

你发现没有我们的`_check_events()`方法变得越来越臃肿了，那我们有什么好的方法可以让代码看起来简洁一点的吗？诶，对了，我们可以将管理将键盘按下的事件和键盘松开的按键分开，这样的话会让我们的`_check_events()`更加有逻辑哦，所以我们分别从两个方面进行代买重构。

### 重构`_check_keyup_events()`

> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 让飞船往右边移动
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            
            elif event.type == pygame.KEYUP:
            # 注意：改这里--------------------------------
                _check_keyup_events(event)
            # 注意：改这里--------------------------------
    
    # 注意：改这里--------------------------------
    def _check_keyup_events(self, event):
        """Events handler for keyup"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    # 注意：改这里--------------------------------

```

### 重构`_check_keydown_events()`

> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
            # 注意：改这里--------------------------------
                self._check_keydown_events(event)
            # 注意：改这里--------------------------------
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # 注意：改这里--------------------------------
    def _check_keydown_events(self, event):
        """Events handler for keydown"""
        if event.key == pygame.K_RIGHT:
            # 让飞船往右边移动
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    # 注意：改这里--------------------------------

```

经过我们对两个方法的重构，你再去看一下`_check_event()`，是不是瞬间干净多了呀！

> 修改的文件名称：`alien_invasion.py`
```python
class AlienInvasion:
    def __init__(self) -> None:
        #上面都一样------------------------------
    
    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

```

**学习标注**：在以后的学习过程中，当我们发现我们的代码量越来越多的时候，看的时候头痛脑胀的时候，那就是最好的时候可以对自己的代码进行重构了，这是一个很好的习惯也是一种很重要的技能哦。