import cv2
import itertools, os
import numpy as np
from ocr_model import build_model
from parameter import letters
import pandas as pd
import os

# ignore tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

ar_to_en = {"١": "1", "٢": "2", "٣": "3", "٤": "4", "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9", "٠": "0",
            "أ": "A", "ب": "B", "ج": "G", "ح": "H", "د": "D", "ر": "R", "س": "C", "ص": "S", "ط": "T", "ع": "E", "ف": "F", "ق": "Q", "ك": "K", "ل": "L", "م": "M", "ن": "N", "ه": "O", "و": "W", "ى": "Y"}

en_to_ar = {v: k for k, v in ar_to_en.items()}



max_letters = 7
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
def label_to_en(label):
    new = ""
    for l in label:
        if l == " ":
            continue
        elif l in digits:
            new += l
        else:
            try:
                new = new + ar_to_en[l]
            except:
                continue
    
    missing = max_letters - len(new)
    if missing > 0:
        new = new + "X" * missing
    return new

def reverse_str(s):
    return s[::-1]

def label_to_ar(label):
    label = reverse_str(label)
    ar_label = ""
    for i in label:
        if i == "X":
            continue
        else:
            ar_label += en_to_ar[i]+" "
    return ar_label


def get_label(idxes):
    label = ""
    for idx in idxes:
        if idx < len(letters):
            label += letters[idx]
    return label

def decode_label(out):
    out_best = list(np.argmax(out[0, 2:], axis=1))  # get max index -> len = 32
    #print(out_best)
    out_best = [k for k, g in itertools.groupby(out_best)]  # remove overlap value
    outstr = ''
    for i in out_best:
        if i < len(letters):
            outstr += letters[i]
    return outstr

class PlatesReader:
    def __init__(self, weights) -> None:
        self.model = build_model(False)
        self.model.load_weights(weights)
        self.letters = letters
        self.ar_to_en = {"١": "1", "٢": "2", "٣": "3", "٤": "4", "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9", "٠": "0",
            "أ": "A", "ب": "B", "ج": "G", "ح": "H", "د": "D", "ر": "R", "س": "C", "ص": "S", "ط": "T", "ع": "E", "ف": "F", "ق": "Q", "ك": "K", "ل": "L", "م": "M", "ن": "N", "ه": "O", "و": "W", "ى": "Y"}

        self.en_to_ar = {v: k for k, v in ar_to_en.items()}
        
    def read_plate(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (128, 64))
        img = img.astype(np.float32)
        img = (img / 255.0)
        img = img.T
        img = np.expand_dims(img, axis=-1)
        img = np.expand_dims(img, axis=0)

        net_out_value = self.model.predict(img, verbose=2)
        pred_texts = self.decode_label(net_out_value)
        #pred_texts = self.label_to_ar(pred_texts)
        if len(pred_texts) < 7:
            return None
        return pred_texts
    
    def decode_label(self, out):
        out_best = list(np.argmax(out[0, 2:], axis=1))  # get max index -> len = 32
        #print(out_best)
        out_best = [k for k, g in itertools.groupby(out_best)]  # remove overlap value
        outstr = ''
        for i in out_best:
            if i < len(self.letters):
                outstr += self.letters[i]
        return outstr
    
    def label_to_ar(self, label):
        label = label[::-1]
        ar_label = ""
        for i in label:
            if i == "X":
                continue
            else:
                ar_label += en_to_ar[i]+" "
        ar_label = ar_label.strip()
        return ar_label

