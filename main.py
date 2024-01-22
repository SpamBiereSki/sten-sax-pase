import tkinter as tk
import random
import math

CANVAS_SIZE = 500
RADIUS = 10

OBJ_TYPES =  {
    0: {
        "color": "black",
        "name": "rock",
        "weakness": 2
    },
    1: {
        "color": "red",
        "name": "scissors",
        "weakness": 0
    },
    2: {
        "color": "white",
        "name": "paper",
        "weakness": 1
    },

}


def distance(x_1, y_1, x_2, y_2):
    return math.dist([x_1, y_1], [x_2, y_2])


class SSPObject:
    def __init__(self, obj_type, canvas, coordx=0, coordy=0) -> None:
        self.obj_type = obj_type
        self.x_speed = random.randint(-10,10)
        self.y_speed = random.randint(-10,10)
        self.shape = canvas.create_oval(
            coordx-RADIUS, coordy-RADIUS, coordx+RADIUS, coordy+RADIUS, fill=OBJ_TYPES[self.obj_type]["color"])
        
    def move(self, canvas):
        pos = canvas.coords(self.shape)
        if pos[2]>= CANVAS_SIZE or pos[0] <= 0:
            self.x_speed *= -1
        if pos[3] >= CANVAS_SIZE or pos[1] <= 0:
            self.y_speed *= -1
        canvas.move(self.shape, self.x_speed, self.y_speed)

    def convert(self, canvas):
        self.obj_type = OBJ_TYPES[self.obj_type]["weakness"]
        canvas.itemconfig(self.shape, fill=OBJ_TYPES[self.obj_type]["color"])
    
    def get_center(self, canvas):
        pos = canvas.coords(self.shape)
        x = (pos[0] + pos[2]) / 2
        y = (pos[1] + pos[3]) / 2
        return x, y
    
    def detect_collide(self, foreign_object, canvas):
        x, y = self.get_center(canvas)
        x_f, y_f = foreign_object.get_center(canvas)

        if distance(x, y, x_f, y_f) <= RADIUS:
            return True
    
    def change_speed(self, new_x_speed=None, new_y_speed=None):
        if new_x_speed:
            self.x_speed = new_x_speed
        if new_y_speed:
            self.y_speed = new_y_speed

class Game:
    def __init__(self, amount_each=10,) -> None:
        self.tk = tk.Tk()
        self.canvas = tk.Canvas(
            self.tk, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="grey"
        )
        self.canvas.pack()
        self.objects = self.create_objects(amount_each)
        self.update_objects()
        self.tk.mainloop()

    def create_objects(self, amount_each):
        object_list = []

        for i in range(3):
            for _ in range(amount_each):
                theta = (random.random() + i )* 2 * math.pi / 3 
                r = random.random() * (CANVAS_SIZE / 2 - CANVAS_SIZE / 4) + CANVAS_SIZE / 4
                x_coord = math.floor(r * math.cos(theta)) + CANVAS_SIZE / 2
                y_coord = math.floor(r * math.sin(theta)) + CANVAS_SIZE / 2
                object_list.append(SSPObject(i, self.canvas, x_coord, y_coord))

        return object_list 
    
    def update_objects(self):
        for i in range(len(self.objects)):
            # detect collisions
            curr_obj = self.objects[i]

            for j in range(i+1, len(self.objects)):
                curr_foreign_obj = self.objects[j]
                did_collide = curr_obj.detect_collide(curr_foreign_obj, self.canvas)
                if did_collide:
                    curr_obj.change_speed(
                        new_x_speed = (- 1) * curr_obj.x_speed ,
                        new_y_speed = (- 1) * curr_obj.y_speed ,
                    )
                    curr_foreign_obj.change_speed(
                        new_x_speed = (- 1) * curr_foreign_obj.x_speed,
                        new_y_speed = (- 1) * curr_foreign_obj.y_speed ,
                    )
                    if curr_obj.obj_type == curr_foreign_obj.obj_type:
                        pass
                    elif OBJ_TYPES[curr_obj.obj_type]["weakness"] == curr_foreign_obj.obj_type:
                        curr_obj.convert(self.canvas)
                    else:
                        curr_foreign_obj.convert(self.canvas)
            curr_obj.move(self.canvas)
        self.tk.after(50, self.update_objects)


if __name__ == "__main__":
    game = Game()