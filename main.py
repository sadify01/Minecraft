from ursina import *
from ursina.shaders import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor
import random


app = Ursina()
player = FirstPersonController()
noise = PerlinNoise(octaves=1,seed=42069)
sky = Sky()
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.fullscreen = True

player.visible = False
player.model = 'steve.obj'
player.origin_y = -0.8
player.cursor.color = color.white
player.cursor.texture = 'cursor.png'
player.cursor.rotation_z = 0
player.cursor.scale = 0.025
player.height = 1.62
player.camera_pivot.y = player.height
player.jump_height = 1.252
player.jump_up_duration = 0.6
player.gravity = 0.8
camera.fov = 100
enabled = True
placing = False
placeable = True
switching = False
switchable = True
played = False
attack = 0

grassSoundOptions = ['grass1.ogg','grass2.ogg','grass3.ogg','grass4.ogg']
stoneSoundOptions = ['stone1.ogg','stone2.ogg','stone3.ogg','stone4.ogg']
woodSoundOptions = ['wood1.ogg','wood2.ogg','wood3.ogg','wood4.ogg']
leavesSoundOptions = ['grass1.ogg','grass2.ogg','grass3.ogg','grass4.ogg']
obsidianSoundOptions = ['stone1.ogg','stone2.ogg','stone3.ogg','stone4.ogg']

stepOnGrassSoundOptions = ['grass5.ogg','grass6.ogg','grass7.ogg','grass8.ogg','grass9.ogg','grass10.ogg']
stepOnStoneSoundOptions = ['stone5.ogg','stone6.ogg','stone7.ogg','stone8.ogg','stone9.ogg','stone10.ogg']
stepOnWoodSoundOptions = ['wood5.ogg','wood6.ogg','wood7.ogg','wood8.ogg','wood9.ogg','wood10.ogg']
stepOnLeavesSoundOptions = ['grass5.ogg','grass6.ogg','grass7.ogg','grass8.ogg','grass9.ogg','grass10.ogg']
stepOnObsidianSoundOptions = ['stone5.ogg','stone6.ogg','stone7.ogg','stone8.ogg','stone9.ogg','stone10.ogg']

explosionSoundOptions = ['explosion1.ogg','explosion2.ogg','explosion3.ogg','explosion4.ogg']

creeperSoundOptions = ['creeper1.ogg']

creeperHurtOptions = ['creeper_hurt1.ogg','creeper_hurt2.ogg','creeper_hurt3.ogg','creeper_hurt4.ogg']
chickenHurtOptions = ['chicken_hurt1.ogg','chicken_hurt2.ogg']
endermanHurtOptions = ['enderman_hurt1.ogg','enderman_hurt2.ogg','enderman_hurt3.ogg','enderman_hurt4.ogg']
ghastHurtOptions = ['ghast_hurt1.ogg','ghast_hurt2.ogg','ghast_hurt3.ogg','ghast_hurt4.ogg','ghast_hurt5.ogg']

creeperDeathOptions = ['creeper_death.ogg']
chickenDeathOptions = ['chicken_hurt1.ogg','chicken_hurt2.ogg']
endermanDeathOptions = ['enderman_death.ogg']
ghastDeathOptions = ['ghast_death.ogg']

weakAttackOptions = ['weak_attack1.ogg','weak_attack2.ogg','weak_attack3.ogg','weak_attack4.ogg']
sweepAttackOptions = ['sweep_attack1.ogg','sweep_attack2.ogg','sweep_attack3.ogg','sweep_attack4.ogg','sweep_attack5.ogg','sweep_attack6.ogg','sweep_attack7.ogg']

sword = ['sword.obj','sword.png',0.5,-1,grassSoundOptions,"sword",0.02,90,60,0,0.70,-0.30]
grass = ['grass.obj','grass.png',0.5,0.5,grassSoundOptions,"grass",0.2,-20,10,30,0.85,-0.65]
stone = ['cube','stone.png',1,-0.25,stoneSoundOptions,"stone",0.4,-20,10,30,0.85,-0.65]
wood = ['wood.obj','wood.png',0.625,0.4,woodSoundOptions,"wood",0.25,-20,10,30,0.85,-0.65]
leaves = ['leaves.obj','leaves.png',0.625,0.4,leavesSoundOptions,"leaves",0.25,-20,10,30,0.85,-0.65]
obsidian = ['obsidian.obj','obsidian.png',0.625,0.4,obsidianSoundOptions,"obsidian",0.25,-20,10,30,0.85,-0.65]

slot1 = sword
slot2 = grass
slot3 = stone
slot4 = wood
slot5 = leaves
slot6 = obsidian
slot7 = None
slot8 = None
slot9 = None
currentSlot = slot1

terrainWidth = 32
amp = 12
freq = 24
boxes = []
for i in range(terrainWidth*terrainWidth):
    box = Button(
        color=color.white,
        shader=basic_lighting_shader,
        parent=scene
    )
    box.x = floor(i/terrainWidth)
    box.z = floor(i%terrainWidth)
    box.y = floor((noise([box.x/freq,box.z/freq]))*amp)
    if box.y > 1:
        box.model = 'cube'
        box.texture = 'stone.png'
        box.scale = 1
        box.origin_y = -0.25
        box.block_type = "stone"
    else:
        box.model = 'grass.obj'
        box.texture = 'grass.png'
        box.scale = 0.5
        box.origin_y = 0.5
        box.block_type = "grass"
    boxes.append(box)

player.x = terrainWidth/2
player.z = terrainWidth/2
player.y = box.y+2

heldBlock = Entity(
    model=currentSlot[0],
    texture=currentSlot[1],
    shader=lit_with_shadows_shader,
    rotation_x=currentSlot[7],
    rotation_z=currentSlot[8],
    rotation_y=currentSlot[9],
    x=currentSlot[10],
    y=currentSlot[11],
    scale=currentSlot[6],
    origin_y=currentSlot[3],
    parent=camera.ui
)

hud = Entity(
    model='hud.obj',
    texture='hud.png',
    rotation_y = (90),
    parent=camera.ui
)
hud.scale = 0.035
hud.y = -0.5 + (hud.scale_y*0.5)

inventory = Entity(
    model='quad',
    texture='inventory.png',
    parent=camera.ui
)
inventory.scale = 0.55
inventory.visible = False

mobs = []

creeper = Entity(
    model='creeper.obj',
    texture='creeper.png',
    rotation=(0,-135,0),
    scale=(0.08),
    x=(20),
    z=(20),
    origin_y=-9.8,
    collider='box',
    double_sided=True,
    explode=False,
    mob_type="creeper",
    isDead=False,
    hp=20
)
mobs.append(creeper)

vincent = Entity(
    model='chicken.obj',
    texture='chicken.png',
    rotation=(0,-90,0),
    scale=(0.05),
    x=(11),
    y=(2),
    z=(11),
    origin_y=-2.5,
    collider='box',
    double_sided=True,
    direction="positive",
    mob_type="chicken",
    isDead=False,
    hp=4
)
mobs.append(vincent)

endre = Entity(
    model='enderman.obj',
    texture='enderman.png',
    rotation=(0,180,0),
    scale=(0.055),
    x=random.randint(0,31),
    z=random.randint(0,31),
    origin_y=-21.9,
    collider='box',
    double_sided=True,
    mob_type="enderman",
    isDead=False,
    hp=40
)
mobs.append(endre)

ghast = Entity(
    model='ghast.obj',
    texture='ghast.png',
    rotation_y=(-90),
    scale=(0.5),
    x=(100),
    y=(25),
    z=(100),
    collider='box',
    double_sided=True,
    direction="negative",
    mob_type="ghast",
    isDead=False,
    hp=10
)
mobs.append(ghast)

backgroundMusic = Audio(
    'background_music.mp3',
    volume=0.3-0.2,
    autoplay=True,
    loop=True,
)

creeperSound = Audio(
    random.choice(creeperSoundOptions),
    volume=0.5,
    autoplay=False,
    loop=False
)

explosionSound = Audio(
    random.choice(explosionSoundOptions),
    volume=0.5,
    autoplay=False,
    loop=False
)

pX = player.x
pZ = player.z

def update():
    global pX
    global pZ
    global ghast
    global placing
    global placeable
    global switching
    global switchable
    global creeperSound
    global stepSound
    global played
    global attack

    if attack < 1:
        attack += 1.6 * time.dt

    if abs(player.x-pX)>1.5 or abs(player.z-pZ)>1.5:
        pX=player.x
        pZ=player.z
        for box in boxes:
            if box.x == round(player.x) and box.z == round(player.z) and box.y == round(player.y)-1:
                if box.block_type == "grass":
                    stepSound = random.choice(stepOnGrassSoundOptions)
                elif box.block_type == "stone":
                    stepSound = random.choice(stepOnStoneSoundOptions)
                elif box.block_type == "wood":
                    stepSound = random.choice(stepOnWoodSoundOptions)
                elif box.block_type == "leaves":
                    stepSound = random.choice(stepOnLeavesSoundOptions)
                elif box.block_type == "obsidian":
                    stepSound = random.choice(stepOnObsidianSoundOptions)

                currentStepSound = Audio(
                    stepSound,
                    volume=0.5,
                    autoplay=False,
                    loop=False
                )
                currentStepSound.play()

    if held_keys['w'] and held_keys['control']:
        player.speed = 6
        if camera.fov < 110:
            camera.fov += 50 * time.dt
    else:
        player.speed = 4.3
        if camera.fov > 100:
            camera.fov -= 50 * time.dt

    if currentSlot == sword:
        if placeable == True:
            if placing == True:
                switchable = False
                if heldBlock.x > 0.30 and heldBlock.y > -0.50:
                    heldBlock.x -= 0.1 * 20 * time.dt
                    heldBlock.y -= 0.1 * 10 * time.dt
                    heldBlock.rotation_x += 15 * 20 * time.dt
                    heldBlock.rotation_z += 10 * 20 * time.dt
                    heldBlock.rotation_y += 0 * 20 * time.dt
                    if heldBlock.x < 0.50 and heldBlock.y < -0.40:
                        placing = False

            if placing == False:
                if heldBlock.x < 0.70 and heldBlock.y < -0.30:
                    heldBlock.x += 0.1 * 20 * time.dt
                    heldBlock.y += 0.1 * 10 * time.dt
                    heldBlock.rotation_x -= 15 * 20 * time.dt
                    heldBlock.rotation_z -= 10 * 20 * time.dt
                    heldBlock.rotation_y += 0 * 20 * time.dt
                    if heldBlock.x > 0.70 and heldBlock.y > -0.30:
                        heldBlock.x = 0.70
                        heldBlock.y = -0.30
                        heldBlock.rotation_x = 90
                        heldBlock.rotation_z = 60
                        heldBlock.rotation_y = 0
                        switchable = True

        if switchable == True:
            if switching == True:
                placeable = False
                if heldBlock.y > -0.90:
                    heldBlock.y -= 0.1 * 90 * time.dt
                    if heldBlock.y < -0.90:
                        switching = False

            if switching == False:
                if heldBlock.y < -0.30:
                    heldBlock.y += 0.1 * 90 * time.dt
                    if heldBlock.y > -0.30:
                        heldBlock.y = -0.30
                        heldBlock.rotation_x = 90
                        heldBlock.rotation_z = 60
                        heldBlock.rotation_y = 0
                        placeable = True

    else:
        if placeable == True:
            if placing == True:
                switchable = False
                if heldBlock.x > 0.45 and heldBlock.y > -0.85:
                    heldBlock.x -= 0.1 * 40 * time.dt
                    heldBlock.y -= 0.1 * 20 * time.dt
                    heldBlock.rotation_x += 0 * 40 * time.dt
                    heldBlock.rotation_z -= 10 * 40 * time.dt
                    heldBlock.rotation_y -= 10 * 40 * time.dt
                    if heldBlock.x < 0.45 and heldBlock.y < -0.85:
                        placing = False

            if placing == False:
                if heldBlock.x < 0.85 and heldBlock.y < -0.65:
                    heldBlock.x += 0.1 * 40 * time.dt
                    heldBlock.y += 0.1 * 20 * time.dt
                    heldBlock.rotation_x += 0 * 40 * time.dt
                    heldBlock.rotation_z += 10 * 40 * time.dt
                    heldBlock.rotation_y += 10 * 40 * time.dt
                    if heldBlock.x > 0.85 and heldBlock.y > -0.65:
                        heldBlock.x = 0.85
                        heldBlock.y = -0.65
                        heldBlock.rotation_x = -20
                        heldBlock.rotation_z = 10
                        heldBlock.rotation_y = 30
                        switchable = True

        if switchable == True:
            if switching == True:
                placeable = False
                if heldBlock.y > -0.90:
                    heldBlock.y -= 0.1 * 30 * time.dt
                    if heldBlock.y < -0.90:
                        switching = False

            if switching == False:
                if heldBlock.y < -0.65:
                    heldBlock.y += 0.1 * 30 * time.dt
                    if heldBlock.y > -0.65:
                        heldBlock.y = -0.65
                        heldBlock.rotation_x = -20
                        heldBlock.rotation_z = 10
                        heldBlock.rotation_y = 30
                        placeable = True

    if player.y < -25:
        player.x = terrainWidth/2
        player.z = terrainWidth/2
        player.y = -2

    if ghast.direction == "negative":
        ghast.x -= 5 * time.dt
    if ghast.direction == "positive":
        ghast.x += 5 * time.dt

    if ghast.x < -terrainWidth * 2:
        ghast.rotation_y = 90
        ghast.direction = "positive"
    if ghast.x > terrainWidth * 3:
        ghast.rotation_y = -90
        ghast.direction = "negative"

    for box in boxes:
        if box.x == round(creeper.x) and box.z == round(creeper.z) and box.y + 1 < creeper.y:
            creeper.y -= 1 * 3 * time.dt
        if box.x == round(creeper.x) and box.z == round(creeper.z) and box.y + 1 > creeper.y:
            creeper.y += 1 * 3 * time.dt

        if box.x == round(vincent.x) and box.z == round(vincent.z) and box.y + 1 < vincent.y:
            vincent.y -= 1 * 3 * time.dt
        if box.x == round(vincent.x) and box.z == round(vincent.z) and box.y + 1 > vincent.y:
            vincent.y += 1 * 3 * time.dt

        if box.x == round(endre.x) and box.z == round(endre.z):
            endre.y = box.y + 1

    if creeper.visible == True:
        if creeper.x + 3 > player.x and creeper.z + 3 > player.z:
            if creeper.x - 3 < player.x and creeper.z - 3 < player.z:
                if played == False:
                    if creeperSound.playing == False:
                        creeperSound.play()
                        played = True

        if creeperSound.playing == False:
            if creeper.x + 3 < player.x or creeper.z + 3 < player.z or creeper.x - 3 > player.x or creeper.z - 3 > player.z:
                played = False
            elif creeper.x + 3 > player.x and creeper.z + 3 > player.z and creeper.x - 3 < player.x and creeper.z - 3 < player.z:
                creeper.explode = True

    if creeper.explode == True:
        for box in boxes:
            if box.x < creeper.x + 3 and box.z < creeper.z + 3:
                if box.x > creeper.x - 3 and box.z > creeper.z - 3:
                    creeper.visible = False
                    explosionSound.play()
                    boxes.remove(box)
                    destroy(box)

    if vincent.direction == "negative":
        vincent.x += 0.5 * time.dt
    if vincent.direction == "positive":
        vincent.x -= 0.5 * time.dt

    if vincent.x > 29:
        vincent.rotation_y = -90
        vincent.direction = "positive"
    if vincent.x < 5:
        vincent.rotation_y = 90
        vincent.direction = "negative"

    creeper.look_at(player)
    creeper.rotation_x = 0
    creeper.rotation_z = 0

    endre.look_at(player)
    endre.rotation_x = 0
    endre.rotation_z = 0


def input(key):
    global enabled
    global placing
    global switching
    global currentSlot
    global hurtSound
    global attack

    if key == 'left mouse down':
        placing = True

    if key == 'right mouse down':
        placing = True

    if key == '1':
        switching = True
        currentSlot = slot1
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '2':
        switching = True
        currentSlot = slot2
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '3':
        switching = True
        currentSlot = slot3
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '4':
        switching = True
        currentSlot = slot4
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '5':
        switching = True
        currentSlot = slot5
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '6':
        switching = True
        currentSlot = slot6
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '7':
        switching = True
        currentSlot = slot7
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '8':
        switching = True
        currentSlot = slot8
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]
    if key == '9':
        switching = True
        currentSlot = slot9
        heldBlock.model = currentSlot[0]
        heldBlock.texture = currentSlot[1]
        heldBlock.scale = currentSlot[6]
        heldBlock.origin_y = currentSlot[3]
        heldBlock.rotation_x = currentSlot[7]
        heldBlock.rotation_z = currentSlot[8]
        heldBlock.rotation_y = currentSlot[9]
        heldBlock.x = currentSlot[10]
        heldBlock.y = currentSlot[11]

    if key == 'q':
        if camera.z == 0:
            camera.z = -3
            player.visible = True
        else:
            camera.z = 0
            player.visible = False

    if key == 'e':
        Entity.disable(player)
        inventory.visible = True
        enabled = False

    if key == 'escape':
        if enabled == True:
            quit()
        elif enabled == False:
            Entity.enable(player)
            inventory.visible = False
            enabled = True

    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                if currentSlot == sword:
                    weakAttack = random.choice(weakAttackOptions)

                    currentWeakAttack = Audio(
                        weakAttack,
                        volume=0.5,
                        autoplay=False,
                        loop=False
                    )
                    currentWeakAttack.play()
                else:
                    placingSound = random.choice(currentSlot[4])

                    currentPlacingSound = Audio(
                    placingSound,
                    volume=0.5,
                    autoplay=False,
                    loop=False,
                    )
                    currentPlacingSound.play()

                    new = Button(
                        color=color.white,
                        model=currentSlot[0],
                        texture=currentSlot[1],
                        shader=basic_lighting_shader,
                        position=box.position + mouse.normal,
                        scale=currentSlot[2],
                        parent=scene,
                        origin_y=currentSlot[3],
                        block_type = currentSlot[5]
                    )
                    boxes.append(new)

            if key == 'right mouse down':
                if box.block_type == "grass":
                    breakingSound = random.choice(grassSoundOptions)
                if box.block_type == "stone":
                    breakingSound = random.choice(stoneSoundOptions)
                if box.block_type == "wood":
                    breakingSound = random.choice(woodSoundOptions)
                if box.block_type == "leaves":
                    breakingSound = random.choice(leavesSoundOptions)
                if box.block_type == "obsidian":
                    breakingSound = random.choice(obsidianSoundOptions)

                currentBreakingSound = Audio(
                breakingSound,
                volume=0.5,
                autoplay=False,
                loop=False,
                )
                currentBreakingSound.play()
                boxes.remove(box)
                destroy(box)

    for mob in mobs:
        if mob.hovered:
            if key == 'left mouse down':
                if mob.mob_type == "creeper":
                    hurtSound = random.choice(creeperHurtOptions)
                    deathSound = random.choice(creeperDeathOptions)
                if mob.mob_type == "chicken":
                    hurtSound = random.choice(chickenHurtOptions)
                    deathSound = random.choice(chickenDeathOptions)
                if mob.mob_type == "enderman":
                    hurtSound = random.choice(endermanHurtOptions)
                    deathSound = random.choice(endermanDeathOptions)
                if mob.mob_type == "ghast":
                    hurtSound = random.choice(ghastHurtOptions)
                    deathSound = random.choice(ghastDeathOptions)

                if currentSlot == sword:
                    if attack >= 1:
                        attack = 0
                        mob.hp -= 7

                        sweepAttackSound = random.choice(sweepAttackOptions)
                        currentSweepAttackSound = Audio(
                            sweepAttackSound,
                            volume=0.5,
                            autoplay=False,
                            loop=False
                        )
                        currentSweepAttackSound.play()

                        if mob.hp <= 0:
                            mob.isDead = True

                        if mob.isDead == False:
                            currentHurtSound = Audio(
                                hurtSound,
                                volume=0.5,
                                autoplay=False,
                                loop=False
                            )
                            currentHurtSound.play()
                    elif attack < 1:
                        mob.hp -= 0
                else:
                    if attack >= 1:
                        attack = 0
                        mob.hp -= 1

                        weakAttackSound = random.choice(weakAttackOptions)
                        currentWeakAttackSound = Audio(
                            weakAttackSound,
                            volume=0.5,
                            autoplay=False,
                            loop=False
                        )
                        currentWeakAttackSound.play()

                        if mob.hp <= 0:
                            mob.isDead = True

                        if mob.isDead == False:
                            currentHurtSound = Audio(
                                hurtSound,
                                volume=0.5,
                                autoplay=False,
                                loop=False
                            )
                            currentHurtSound.play()

                if mob.isDead == True:
                    currentDeathSound = Audio(
                        deathSound,
                        volume=0.5,
                        autoplay=False,
                        loop=False
                    )
                    currentDeathSound.play()

                    mob.collider = None
                    mob.visible = False
                    mobs.remove(mob)


app.run()