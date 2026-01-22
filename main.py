import ursina as ur
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import threading as th
import Melvicontrol



class Daddy(ur.Entity):
    def __init__(self, position=(0, 0, 0), rotation=(0, 90, 0), scale=0.02, spawn_high=True, **kwargs):
        if spawn_high: 
            position = (position[0], position[1] + 100, position[2])
        super().__init__(position=position, world_rotation=rotation+(-90, 0, -90), shader=lit_with_shadows_shader, scale=scale, **kwargs)
        
        self.BODY = ur.Entity(
            parent=self,
            model='Body.stl',
            shader=lit_with_shadows_shader,
            collider="mesh",
            position=(0, 0, 10),
            color=ur.color.hex("#3D3A3A")
        )

        self.SIGN = ur.Entity(
            parent=self,
            model='Shield.obj',
            texture="50kmh.png",
            scale=10,
            world_position=self.BODY.world_position,
            shader=lit_with_shadows_shader,
            collider="mesh",
            #color=ur.color.hex("#3D3A3A")
        )
        if spawn_high:
            self.animate_y(0, duration=3, delay=0.1, curve=ur.curve.out_bounce)

class Speedometer(ur.Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        super().__init__(parent=ur.camera.ui, model='cube', texture='Adobe Express - file.png', position=position, scale=(0.4, 0.2), **kwargs)
        self.pointer = ur.Entity(
            parent=ur.camera.ui,
            model='cube', 
            color=ur.color.red, 
            position=(-0.61, -0.485, -1),
            scale=(0.01, 0.15, 0.05), 
            origin_y=-0.5, 
            rotation_z=-90
        )
        self.speed = 0
    
    def update(self):        
        target_angle = -90 + (self.speed / 100) * 180
        self.pointer.rotation_z = ur.lerp(self.pointer.rotation_z, target_angle, 0.1)



class Car(ur.Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lst = []
        self.speed = 0
        self.max_speed = 0.8
        self.acceleration = 0.01
        self.friction = 0.005
        self.already_stopping = True

    def drive(self, forward_backward, left_right):
        #ur.time.sleep(0.05) #Counteract the delay from the esp code to avoid input stacking

        if forward_backward > 0:
            self.speed += self.acceleration
            th.Thread(target=Melvicontrol.drive_up).start()
            self.already_stopping = False
        elif forward_backward < 0:
            self.speed -= self.acceleration
            th.Thread(target=Melvicontrol.drive_down).start()
            self.already_stopping = False
        else:
            if self.speed > 0:
                self.speed -= self.friction
                if self.speed < 0: self.speed = 0
            elif self.speed < 0:
                self.speed += self.friction
                if self.speed > 0: self.speed = 0
            # If no input is given, we should probably tell the robot to stop/coast
            # For now, simplistic approach: if moving very slowly or stopped, ensure remote is stopped
            if abs(self.speed) < 0.01 and not self.already_stopping:
                 th.Thread(target=Melvicontrol.stop).start()
                 self.already_stopping = True
        
        self.speed = ur.clamp(self.speed, -0.3, self.max_speed)

        
        turn_speed = 0.5
        if abs(self.speed) > 0.01:
            direction = 1 if self.speed > 0 else -1
            player.rotation_y += left_right * turn_speed * direction
            
            if left_right < 0:
                th.Thread(target=Melvicontrol.drive_left).start()
            elif left_right > 0:
                th.Thread(target=Melvicontrol.drive_right).start()
        
        player.position += player.forward * self.speed

    def update_animation(self):
        while True:
            events = Melvicontrol.get_events()
            for event in events:
                if event == "SPAWN_SIGN_50":
                    print("Spawning Sign due to YOLO detection!")
                    ur.invoke(lambda: Daddy(position=(player.x + player.forward[0]*2, -0.19, player.z + player.forward[2]*2), rotation=(0, player.rotation_y + 180, 0)))

            forward_backward = 0 if (('s' not in self.lst and 'w' not in self.lst) or ('s' in self.lst and 'w' in self.lst)) else (1 if 'w' in self.lst else -1)
            left_right = 0 if (('a' not in self.lst and 'd' not in self.lst) or ('a' in self.lst and 'd' in self.lst)) else (1 if 'd' in self.lst else -1)
            self.drive(forward_backward, left_right)
            
            if hasattr(self, 'speedometer'):
                self.speedometer.speed = (abs(self.speed) / self.max_speed) * 100
            ur.time.sleep(0.016)  # Approx 60 FPS
            

    def input(self, key):
        if len(key) == 1:
            self.lst.append(key.replace(" down",""))
        try: 
            if key.endswith(" up"):
                self.lst.remove(key.replace(" up",""))
        except ValueError:
            pass



def input(key):
    if key == 'escape' or key == 'q':
        ur.application.quit()
    if key == "up arrow":
        player.y += 0.1 
    if key == "down arrow":
        player.y -= 0.1
    if key == "space":
        Daddy(position=car.world_position+player.forward*10, rotation=car.world_rotation)
        print(car.world_rotation)
        print(car.world_position)
        print(player.forward)
    text.text = f"{key}; {speedometer.speed:.1f} km/h"
    if key == "f":
        ur.camera.fov = 90 if ur.camera.fov == 30 else 30
    if key == "v":
        ur.camera.position = (0,5,-20) if ur.camera.position == (0, 0, 0) else (0, 0, 0)
        #player.visible = not player.visible
    
        




if __name__ == '__main__':
    app = ur.Ursina(fullscreen=True)
    player = FirstPersonController(gravity=0, position=(0,1,0))

    ground = ur.Entity(model='plane', scale=(100, 1, 100), texture_scale=(100,100), texture='grass', collider='box')
    player.update = None # Disable default movement
    car = Car(parent=player, model="2025_bugatti_bolide", collider="mesh", scale=150, rotation=(0,180,0), shader=lit_with_shadows_shader)
    player.collider = car.collider
    
    speedometer = Speedometer(position=(-0.61, -0.4))
    car.speedometer = speedometer
    
    sky = ur.Sky()
    text = ur.Text(text="None", position=(-0.7,0.45), scale=1.5)
    sign = Daddy(position=(20,-0.19,2))

    threading = th.Thread(target=car.update_animation)
    threading.start()
    app.run()
