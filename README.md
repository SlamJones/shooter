shooter.py is a practice project built by Slam Jones for practice purposes,
to learn Python and programming in general, and to work on problem-solving
and optimization.

shooter.sh is a bash wrapper that modifies keyboard repeat delay, so player
can move smoothly in-game.  When game exits, wrapper sets keyboard repeat delay
back to default value.

It is no longer necessary to lauch the game using shooter.sh;
funtionality has been incorporated into shooter.py.

Shooter is a top-down arcade shooter game.  The player, enemies, pickups,
and projectiles are represented by colored circles of various sizes.

There are now three game modes: Horde, Waves, and Adventure.

Horde is the classis endless game-type; as enemies are killed, new ones 
spawn to take their place.  Over time, mobs become more numerous, and 
increasingly stronger mobs will spawn.  This continues until the player
is killed by the mobs.

Waves will spawn a set number of mobs during gameplay.  Once player has slain
all mobs, they return to the Waves Menu screen, where they can choose to 
either spend their accumulated cash on weapons or upgrades, sell weapons, or
continue to the next wave, which will have more mobs than the previous one.

Adventure mode is similar to waves.  However, instead of a menu, the player
is presented with a basic 'world map,' consisting of a series of connected
nodes.  To reach a node, the player must unlock it.  The player start with
two nodes unlocked: the first node is the 'town' node, which function 
similarly to the Waves Vendor Menu, and allows the player to use their cash
to purchase new weapons or ammo for their current weapons, or sell the
weapons they already have.  Each unlocked node will have more mobs than
the preceding nodes, creating a sense of progression.

Pickups grant new weapons, increase ammo of existing weapons, or restore
some health.  Pickup spawns are controlled by a central function, which waits
to spawn if a pickup is already present.  The spawn controller determines
if a pickup is to be spawned, where to spawn it, what values it has, and how
long it will exist before deacying and disappearing from screen.
Spawns can be affected by player score or other variables.

Weapons come in many forms.  The 'Basic' weapon fires one projectile at a
time at a moderate rate, with Damage of 1.  Other weapons include 'Shotgun',
which spawns 7 pellets in a fan pattern (angle of spread and number of pellets
can be modified at run-time or in the script), 'Shatter', which causes a pellet,
after hitting an object, to become 3 projectiles, spreading out in a fan pattern
from the center of the hit object.  'Wide' fires several parallel projectiles
in the direction the player is facing.  'Split' causes a projectile, upon hitting
an object, to turn into 4 projectiles, radiating outward from hit object.  
'Passthru' determines how many objects it can hit before being destroyed.  Other
weapon types can be created, and weapon types can be combined.  For example,
'Split > Shatter' first creates a 'Split' when hitting an object.  Each of the
created projectiles from the 'Split' will 'Shatter' when encountering an object,
potentially leading to a cascade of projectiles being created.

Player has a 'health' variable that is reduce by 1 (or mobs damage stat) when
they collide with a mob.  Upon collision, player loses 1 health and becomes
intangible(cannot be hit again) for several frames to prevent multiple hits
in a short timespan.  
(Not yet Implemented: Upon player death, game is reset and player can start a new
game.)

Mobs are spawned at the edges of the playfield, and slowly move towards the player.
Each mob killed increases the speed of the other mobs by a small amount.  After X
mobs are killed (default: 10), another mob is added to the 'max_mobs' setting.
So the longer a game goes on, the more mobs will appear on-screen at any given time.
Default 'max_mobs' is 24, but can increase to over 100 if player plays long enough.
When a mob is hit by a projectile, it flashes for a frame for user feedback.  Mob
loses health equal to damage value of projectile.  If mob health reaches 0 or less,
then a death animation is created and queued.  There are two death animations:
'pop,' in which the mobs graphic swells to 3x original size, and 'explode,' in which
the mob takes the direction and speed of the killing projectile, and creates a 'cone'-
like graphic in the inherited projectile, made up of several circles, increasing in size.

==== CURRENT ISSUES ====

Higher numbers of mobs and projectiles creates game lag, and reduces possible frame
rate.  Spawn and collision functions need to be optimized to reduce time taken
per frame, and thus improve and stabilize frame rate.

Animation 'i_flash' does not flash object: instead stays solid "flash" color until
animation ends.
