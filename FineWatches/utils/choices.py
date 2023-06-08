import os
import pandas as pd

DATASET_PATH = 'C:/Users/oliko/OneDrive/Dokumenter/GitHub/FineTimeWear/FineWatches/dataset/Luxury watch.csv'

def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]

df = pd.read_csv(DATASET_PATH, sep=',')

WatchBrandChoices = ModelChoices(df.Brand.unique())
WatchModelChoices = ModelChoices(df.Model.unique())
WatchCaseMaterialChoices = ModelChoices(df['Case Material'].unique())
WatchStrapMaterialChoices = ModelChoices(df['Strap Material'].unique())
WatchMovementTypeChoices = ModelChoices(df['Movement Type'].unique())
WatchWaterResistanceChoices = ModelChoices(df['Water Resistance'].unique())
WatchCaseDiameterChoices = ModelChoices(df['Case Diameter (mm)'].astype(str).unique())
WatchCaseThicknessChoices = ModelChoices(df['Case Thickness (mm)'].astype(str).unique())
WatchBandWidthChoices = ModelChoices(df['Band Width (mm)'].astype(str).unique())
WatchDialColorChoices = ModelChoices(df['Dial Color'].unique())
WatchCrystalMaterialChoices = ModelChoices(df['Crystal Material'].unique())
WatchComplicationChoices = ModelChoices(df.Complications.unique())
WatchPowerReserveChoices = ModelChoices(df['Power Reserve'].astype(str).unique())



UserTypeChoices = ModelChoices(['BrandRep', 'Customer'])

if __name__ == '__main__':
    print(df.item.unique())
    print(WatchBrandChoices.choices())