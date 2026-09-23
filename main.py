import argparse
import copy
import hashlib
import json
import os
import wave
import zipfile
from pathlib import Path

import cv2
import numpy as np
from moviepy import VideoFileClip

parser = argparse.ArgumentParser(description="Convert a video file to a scratch 3.0 project.")
parser.add_argument("video_path", help="Path to input video.")
parser.add_argument("output_path", nargs="?", default="output.sb3", help="Path for generated scratch project. Default is output.sb3.")
parser.add_argument("--color", "-c", default="#0f0f0f", help="Hex color for background. Default is dark gray (#0f0f0f).")
args = parser.parse_args()

BASE_SB3_JSON = {"targets":[{"isStage":True,"name":"Stage","variables":{"FramesVar":["Frames",0],"FPSVar":["FPS",0]},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[],"sounds":[],"volume":100,"layerOrder":0,"tempo":60,"videoTransparency":50,"videoState":"on","textToSpeechLanguage":None},{"isStage":False,"name":"Animation","variables":{},"lists":{},"broadcasts":{},"blocks":{"q2m`E=xC*xgaqkNg!/ow":{"opcode":"looks_switchcostumeto","next":".R.G1rkmC3Vwo.FdUjID","parent":")7$Q_gAqhO@h{(hF*g7i","inputs":{"COSTUME":[3,"w]N$W1B-HS*@S)5=#n!f","}W@t3L|#VfUG6;3D%F72"]},"fields":{},"shadow":False,"topLevel":False},"}W@t3L|#VfUG6;3D%F72":{"opcode":"looks_costume","next":None,"parent":"q2m`E=xC*xgaqkNg!/ow","inputs":{},"fields":{"COSTUME":["1"]},"shadow":True,"topLevel":False},".R.G1rkmC3Vwo.FdUjID":{"opcode":"looks_switchcostumeto","next":"[VS;q7mS%m3sOdiYAA!B","parent":"q2m`E=xC*xgaqkNg!/ow","inputs":{"COSTUME":[3,"sT7M9p8JsWtwdlb1l@}E","79A0QRe9cKR{|[7i4bbb"]},"fields":{},"shadow":False,"topLevel":False},"sT7M9p8JsWtwdlb1l@}E":{"opcode":"operator_subtract","next":None,"parent":".R.G1rkmC3Vwo.FdUjID","inputs":{"NUM1":[1,[4,"0"]],"NUM2":[1,[4,"1"]]},"fields":{},"shadow":False,"topLevel":False},"79A0QRe9cKR{|[7i4bbb":{"opcode":"looks_costume","next":None,"parent":".R.G1rkmC3Vwo.FdUjID","inputs":{},"fields":{"COSTUME":["1"]},"shadow":True,"topLevel":False},"[VS;q7mS%m3sOdiYAA!B":{"opcode":"data_setvariableto","next":"1_Uh[G:|X34UenD|Q;GY","parent":".R.G1rkmC3Vwo.FdUjID","inputs":{"VALUE":[3,"@.ej^DiAcPdko1bR[;qY",[10,"0"]]},"fields":{"VARIABLE":["Frames","FramesVar"]},"shadow":False,"topLevel":False},"@.ej^DiAcPdko1bR[;qY":{"opcode":"operator_add","next":None,"parent":"[VS;q7mS%m3sOdiYAA!B","inputs":{"NUM1":[3,",gu^C69+4MqQ=P|GA^+N",[4,""]],"NUM2":[1,[4,"1"]]},"fields":{},"shadow":False,"topLevel":False},",gu^C69+4MqQ=P|GA^+N":{"opcode":"looks_costumenumbername","next":None,"parent":"@.ej^DiAcPdko1bR[;qY","inputs":{},"fields":{"NUMBER_NAME":["number"]},"shadow":False,"topLevel":False},"1_Uh[G:|X34UenD|Q;GY":{"opcode":"looks_switchcostumeto","next":"UPVWp,O`}sEa%a0SDct1","parent":"[VS;q7mS%m3sOdiYAA!B","inputs":{"COSTUME":[3,"Rf}0=PrX*j$j4vfi8(dK","[Jdbb=esiWXR5n:tW2^t"]},"fields":{},"shadow":False,"topLevel":False},"[Jdbb=esiWXR5n:tW2^t":{"opcode":"looks_costume","next":None,"parent":"1_Uh[G:|X34UenD|Q;GY","inputs":{},"fields":{"COSTUME":["1"]},"shadow":True,"topLevel":False},"UPVWp,O`}sEa%a0SDct1":{"opcode":"sensing_resettimer","next":"+1T5VWJVd:)_2`k)Kp5-","parent":"1_Uh[G:|X34UenD|Q;GY","inputs":{},"fields":{},"shadow":False,"topLevel":False},"+1T5VWJVd:)_2`k)Kp5-":{"opcode":"control_repeat_until","next":None,"parent":"UPVWp,O`}sEa%a0SDct1","inputs":{"CONDITION":[2,"~-/lTR%7JFA%Fkvl=Je^"],"SUBSTACK":[2,"S_R[DS(nz6|SvI)j5%/G"]},"fields":{},"shadow":False,"topLevel":False},"~-/lTR%7JFA%Fkvl=Je^":{"opcode":"operator_equals","next":None,"parent":"+1T5VWJVd:)_2`k)Kp5-","inputs":{"OPERAND1":[3,"6:,LZ+{8aPJ^PPB!iv-`",[10,""]],"OPERAND2":[3,[12,"Frames","FramesVar"],[10,"50"]]},"fields":{},"shadow":False,"topLevel":False},"6:,LZ+{8aPJ^PPB!iv-`":{"opcode":"looks_costumenumbername","next":None,"parent":"~-/lTR%7JFA%Fkvl=Je^","inputs":{},"fields":{"NUMBER_NAME":["number"]},"shadow":False,"topLevel":False},"S_R[DS(nz6|SvI)j5%/G":{"opcode":"looks_switchcostumeto","next":None,"parent":"+1T5VWJVd:)_2`k)Kp5-","inputs":{"COSTUME":[3,"prY-OX4}QE[-maEChRtT","Vy)Kc-?Os^SBk3}@0gnX"]},"fields":{},"shadow":False,"topLevel":False},"prY-OX4}QE[-maEChRtT":{"opcode":"operator_subtract","next":None,"parent":"S_R[DS(nz6|SvI)j5%/G","inputs":{"NUM1":[3,"kE}qVBo[P/3%Op@P*dYk",[4,""]],"NUM2":[3,"Gcl5,;A-gafprRzAb4%3",[4,"0.083333"]]},"fields":{},"shadow":False,"topLevel":False},"kE}qVBo[P/3%Op@P*dYk":{"opcode":"operator_add","next":None,"parent":"prY-OX4}QE[-maEChRtT","inputs":{"NUM1":[1,[4,"1"]],"NUM2":[3,"D6l?Zh6t=!3hB`KH7_G0",[4,""]]},"fields":{},"shadow":False,"topLevel":False},"D6l?Zh6t=!3hB`KH7_G0":{"opcode":"operator_mathop","next":None,"parent":"kE}qVBo[P/3%Op@P*dYk","inputs":{"NUM":[3,"UH*`U]V0zDs5DCa=nq*O",[4,""]]},"fields":{"OPERATOR":["floor"]},"shadow":False,"topLevel":False},"UH*`U]V0zDs5DCa=nq*O":{"opcode":"operator_multiply","next":None,"parent":"D6l?Zh6t=!3hB`KH7_G0","inputs":{"NUM1":[3,"tB%P(XbtTH%5/0I^8V1U",[4,""]],"NUM2":[3,[12,"FPS","FPSVar"],[4,""]]},"fields":{},"shadow":False,"topLevel":False},"tB%P(XbtTH%5/0I^8V1U":{"opcode":"sensing_timer","next":None,"parent":"UH*`U]V0zDs5DCa=nq*O","inputs":{},"fields":{},"shadow":False,"topLevel":False},"Gcl5,;A-gafprRzAb4%3":{"opcode":"operator_divide","next":None,"parent":"prY-OX4}QE[-maEChRtT","inputs":{"NUM1":[1,[4,"1"]],"NUM2":[3,[12,"FPS","FPSVar"],[4,""]]},"fields":{},"shadow":False,"topLevel":False},"Vy)Kc-?Os^SBk3}@0gnX":{"opcode":"looks_costume","next":None,"parent":"S_R[DS(nz6|SvI)j5%/G","inputs":{},"fields":{"COSTUME":["klädsel16"]},"shadow":True,"topLevel":False},"XFtZ*a@eUmd38a+r1y2r":{"opcode":"event_whenflagclicked","next":")7$Q_gAqhO@h{(hF*g7i","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":277,"y":163},"w]N$W1B-HS*@S)5=#n!f":{"opcode":"operator_subtract","next":None,"parent":"q2m`E=xC*xgaqkNg!/ow","inputs":{"NUM1":[1,[4,"1"]],"NUM2":[1,[4,"0"]]},"fields":{},"shadow":False,"topLevel":False},"Rf}0=PrX*j$j4vfi8(dK":{"opcode":"operator_subtract","next":None,"parent":"1_Uh[G:|X34UenD|Q;GY","inputs":{"NUM1":[1,[4,"1"]],"NUM2":[1,[4,"0"]]},"fields":{},"shadow":False,"topLevel":False},")7$Q_gAqhO@h{(hF*g7i":{"opcode":"sound_play","next":"q2m`E=xC*xgaqkNg!/ow","parent":"XFtZ*a@eUmd38a+r1y2r","inputs":{"SOUND_MENU":[1,"affpKuZ1)zSJ}%ISFpzJ"]},"fields":{},"shadow":False,"topLevel":False},"affpKuZ1)zSJ}%ISFpzJ":{"opcode":"sound_sounds_menu","next":None,"parent":")7$Q_gAqhO@h{(hF*g7i","inputs":{},"fields":{"SOUND_MENU":["",None]},"shadow":True,"topLevel":False}},"comments":{},"currentCostume":0,"costumes":[],"sounds":[],"volume":100,"layerOrder":1,"visible":True,"x":0,"y":0,"size":100,"direction":90,"draggable":False,"rotationStyle":"all around"}],"monitors":[{"id":"FPSVar","mode":"default","opcode":"data_variable","params":{"VARIABLE":"FPS"},"spriteName":None,"value":0,"width":0,"height":0,"x":5,"y":5,"visible":False,"sliderMin":0,"sliderMax":100,"isDiscrete":True}],"extensions":[],"meta":{"semver":"3.0.0","vm":"15.1.1","agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"}}
temp_dir = "temp"

output_path = args.output_path

def remove_temp_dir():
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(temp_dir)

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
else:
    remove_temp_dir()
    os.makedirs(temp_dir, exist_ok=True)

if os.path.exists(output_path):
    os.remove(output_path)

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def generate_sb3_json(frames_json, sound_json, solid_json, FPS, size):
    sb3_json = copy.deepcopy(BASE_SB3_JSON)
    sb3_json["targets"][0]["costumes"] = [solid_json]
    sb3_json["targets"][1]["costumes"] = frames_json
    if sound_json != None:
        sb3_json["targets"][1]["sounds"] = [sound_json]
        sb3_json["targets"][1]["blocks"]["affpKuZ1)zSJ}%ISFpzJ"]["fields"]["SOUND_MENU"] = [sound_json["name"], None]
    sb3_json["targets"][0]["variables"]["FPSVar"][1] = FPS
    sb3_json["targets"][1]["size"] = size
    sb3_json["targets"][1]["x"] = 0
    sb3_json["targets"][1]["y"] = 0
    return sb3_json

def generate_costume_json(frame_path, width, height):
    return {
        "name":"",
        "dataFormat":Path(frame_path).suffix[1:],
        "assetId":Path(frame_path).stem,
        "md5ext":frame_path,
        "rotationCenterX":width / 2,
        "rotationCenterY":height / 2
    }

def generate_sound_json(sound_path, rate, sample_count):
    return {
        "name":Path(sound_path).stem,
        "assetId":Path(sound_path).stem,
        "dataFormat":Path(sound_path).suffix[1:],
        "rate":rate,
        "sampleCount":sample_count,
        "md5ext":sound_path
    }

def generate_solid_json(width, height, hex_color):
    md5_hash = hashlib.md5(hex_color.encode("utf-8")).hexdigest()
    hex_clean = hex_color.lstrip('#')
    bgr_color = tuple(int(hex_clean[i:i+2], 16) for i in (4, 2, 0))
    solid_img = np.full((height, width, 3), bgr_color, dtype=np.uint8)
    cv2.imwrite(f"{temp_dir}/{md5_hash}.png", solid_img)
    return generate_costume_json(f"{md5_hash}.png", width, height)

def generate_sb3_file(video_path, output_path, solid_color):
    count = 0
    video_capture = cv2.VideoCapture(video_path)
    success, image = video_capture.read()
    costume_json = []
    height, width = image.shape[:2]
    while success:
        print(f"Processed frame {count}", end="\r", flush=True)
        frame_name = f"frame{count}"
        md5_hash = hashlib.md5(frame_name.encode("utf-8")).hexdigest()
        frame_path = os.path.join(temp_dir, f"{md5_hash}.png")
        cv2.imwrite(frame_path, image)
        success, image = video_capture.read()
        count += 1
        costume_json.append(generate_costume_json(f"{md5_hash}.png", width, height))
    video_capture.release()
    print(f"Finished processing frames. frames:{count}")

    print("Generating sound.")
    sound_name = Path(video_path).stem
    md5_hash = hashlib.md5(sound_name.encode("utf-8")).hexdigest()
    sound_path = f"{md5_hash}.wav"
    full_sound_path = os.path.join(temp_dir, sound_path)
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    sound_json = None
    if audio_clip != None:
        audio_clip.write_audiofile(full_sound_path, logger=None)
        with wave.open(full_sound_path, "rb") as wav_file:
            rate = wav_file.getframerate()
            sample_count = wav_file.getnframes()
        sound_json = generate_sound_json(sound_path, rate, sample_count)
        audio_clip.close()
        print("Finished generating sound.")
    else:
        print("No audio found in video.")
    video_clip.close()

    print("Generating solid color.")
    solid_json = generate_solid_json(960, 720, solid_color)
    print("Finished generating solid color.")

    with open(f"{temp_dir}/project.json", "w", encoding="utf-8") as file:
        print("Generating project.json.")
        scale = (min(480/width, 360/height)*2)*100
        json.dump(generate_sb3_json(costume_json, sound_json, solid_json, video_clip.fps, scale), file)
        print("Finished generating project.json.")

    print("Zipping files")
    zip_folder(temp_dir, output_path)
    print(f"Finished generating {output_path}.")

generate_sb3_file(args.video_path, output_path, args.color)
remove_temp_dir()
