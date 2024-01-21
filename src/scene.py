from ray import *
from vec import *
from color import *
from hitinfo import *
from material import *

import json, pathlib, sys
from error import Error

from objects import *



class Scene:
    ## THIS CLASS HOLDS OUR WORLD AND ALL OBJECT INSTANCES
    def __init__(self, ambientLight, useSky):
        self.sky = Sky(ambientLight=ambientLight, useSky=useSky)
        self.objects = []
        self.path = pathlib.Path(__file__).resolve().parent / pathlib.Path("..\\world.json")

    def addObject(self, object):
        self.objects.append(object)

    def load(self, scene):
        self.objects=[]

        if not scene:
            Error.raiseError(
                type="Scene could not be loaded!",
                info="Please enter a valid scene name using the -S argument. Use --help for a list of all options.",
                quitSrc=True
            )

        # open and load world.json
        try:
            with open(self.path, 'r') as world:
                data = json.load(world)[scene]
        except:
            Error.raiseError(
                type="Scene could not be loaded!",
                info="Did you enter the correct scene name? \nScene names are case sensitive.\nCheck for type errors.",
                quitSrc=True
            )
            pass

        # load scene settings
        try:
            self.sky.ambientLighting = listToCol(data["ambient_occlusion"])
            self.sky.useSky = bool(data["use_sky_gradient"])
            self.sky.bendingFac = float(data["sky_bending"])
        except:
            Error.raiseError(
                type="Scene sky setting could not be parsed!",
                info="Please check world.json and try again.",
                quitSrc=True
            )

        # load the objects
        for obj in data["objects"]:
            mat = None

            # parse color
            color = col(.9,.9,.9)
            if obj["type"] != "floor":
                try:
                    color = listToCol(obj["material"]["color"])
                except:
                    Error.raiseError(
                            type=f"Color value of '{obj["type"]}' '{obj["material"]["color"]}' could not be parsed!",
                            info="Please fix world.json and try again",
                            quitSrc=True
                        )
                    
            # parse material
            try:
                match obj["material"]["type"]:
                    case "emissive":
                        mat = Emissive(color)
                    case "lambertian":    
                        mat = Lambertian(color)
                    case "metal":
                        mat = Metal(color, fuzz=int(obj["material"]["fuzz"]))
                       
                    case _:
                        Error.raiseError(
                            type=f"'{obj["material"]["type"]}' is not a valid material!",
                            info="Please fix world.json and try again",
                            quitSrc=True
                        )
            except:
                Error.raiseError(
                    type=f"Material values of '{obj["type"]}' '{obj["material"]["type"]}' could not be parsed!",
                    info="Please fix world.json and try again",
                    quitSrc=True
                )

            # parse object type and add the object
            error = None
            match obj["type"]:
                case "sphere":
                    try:
                        self.addObject(Sphere(
                            pos = listToPoint(obj["position"]),
                            radius = int(obj["radius"]),
                            material = mat
                        ))
                    except:
                        error = "sphere"
                case "floor":
                    try:
                        self.addObject(Floor(
                            pos = listToPoint(obj["position"]),
                            color1 = listToCol(obj["color1"]),
                            color2 = listToCol(obj["color2"]),
                            material = mat
                        ))
                    except:
                        error = "floor"
                case _:
                    Error.raiseError(
                        type=f"'{obj["type"]}' is not a valid object type!",
                        info="Please fix world.json and try again",
                        quitSrc=True
                    )
            if error:
                Error.raiseError(
                    type=f"Failed to parse '{error}' values!",
                    info="Please check your types.",
                    quitSrc=True
                )

