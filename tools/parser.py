﻿from tools import variables as var
from tools import filenames as fl
from tools import logger as log

import subprocess
import shutil
import os

# Import the various file manipulation methods

from tools.methods import *

# Mod installers

def avalanche():
    ExecuteFile(fl.AVALANCHE)

    CopyFolder(var.BOOTLEG_TEMP + "Sprinkles\\AvalancheRepair\\magic", fl.MAGIC_PATCH)

    CopyFile(var.FFVII_PATH + "textures\\Summons\\leviathan", "water_00.png", "water_1_00.png")

def avalanche_gui():
    ExecuteFile(fl.AVALANCHEGUI)

def romeo_mat():
    CopyFolder(var.BOOTLEG_TEMP + "Sprinkles\\Data\\Textures\\Menu\\Romeo14\\Materia_Advent", fl.MODS_FINAL + "menu")

def hardcore_gjoerulv():
    ExtractFile(fl.HARDCORE)

    log.help("SET_LOCATION", "'{0}data'".format(var.FFVII_PATH), "")
    if var.GAME_VERSION in (2012, 2013):
        log.help("PICK_1997_" + str(var.GAME_VERSION))

    shutil.copy(var.BOOTLEG_TEMP + "Sprinkles\\Patch102\\ff7.exe", var.FFVII_PATH + "ff7.exe")

    LaunchFile(fl.HARDCORE, "Gjoerulv.exe")

    for file in ("kernel\\KERNEL.BIN", "kernel\\kernel2.bin", "battle\\scene.bin"):
        shutil.copy(var.FFVII_PATH + "data\\" + file, var.BOOTLEG_TEMP + "hardcore_backup\\" + file)

def aerith_revival():
    ExtractFile(fl.AERISREVIVAL)

    CopyFolder(var.BOOTLEG_TEMP + "Sprinkles\\Revival\\Flevel", var.BOOTLEG_TEMP + fl.AERISREVIVAL)

    shutil.copy(var.FFVII_PATH + "data\\field\\flevel.lgp", fl.FLEVEL_REVIVAL + "flevel.lgp")

def movies():
    if var.MOVIES in range(5, 9): # Rumbah's FMVs
        movies = {5: (7, "RUMBAHSMOOTH1280"), 6: (10, "RUMBAHSHARP1280"), 7: (4, "RUMBAHSMOOTH640"), 8: (4, "RUMBAHSHARP640")}
        max, file = movies[var.MOVIES]
        filef = getattr(fl, file)

        for num in range(1, max):
            FindFile(filef.format(num))

        ExtractFile(filef.format(1), "RumbahFMVs")

        # We got so far, so all the parts do exist and got successfully extracted
        CopyFolder(var.BOOTLEG_TEMP + "RumbahFMVs", var.FFVII_PATH + "movies")
        for mov in ("hit0", "hit1", "off"):
            DeleteFile(var.FFVII_PATH + "movies\\rcket{0}.avi".format(mov))
        RenameFile(var.FFVII_PATH + "movies", ["rckthit0.avi", "rckthit1.avi", "rcktoff.avi"], ["rckethit0.avi", "rckethit1.avi", "rcketoff.avi"])
        return

    for num in range(0, 7): # Install DLPB's videos - add others on top if needed
        FindFile(getattr(fl, "FMVRES" + str(num)))

    # All the files do exist
    log.logger("PARS_INSTALLING", form="FMVRES")
    ExecuteFile(fl.FMVRES0, "/verysilent")
    log.logger("PARS_COMPLETED", form="FMVRES")

    if var.MOVIES == 1: # DLPB's HQ videos
        return

    for part in (1, 2): # Trojak's Enhanced movies
        file = ""
        try:
            for num in range(1, 4):
                FindFile(fl.ENHANCEDMOVIESPARTS.format(num, part))
            if part == 2:
                FindFile(fl.ENHANCEDMOVIESPARTS.format(4, 2))
            file = fl.ENHANCEDMOVIESPARTS.format(1, part)
        except FileNotFoundError:
            try:
                FindFile(fl.ENHANCEDMOVIES.format(part))
                file = fl.ENHANCEDMOVIES.format(part)
            except FileNotFoundError:
                CallSkipMod(fl.ENHANCEDMOVIES.format(part)) # We want to go on and install the rest

        if file:
            log.logger("PARS_INST", form="ENHANCED_MOVIES" + str(part))
            ExtractFile(file, "EnhancedMovies")

    try: # Eidos Logo
        log.logger("PARS_INSTALLING", form="LOGO")
        logo, folder = FindFile(fl.LOGO)
        shutil.copy(folder + logo, var.FFVII_PATH + "movies\\eidoslogo.avi")
        log.logger("PARS_COMPLETED", form="LOGO")
    except FileNotFoundError:
        CallSkipMod(fl.LOGO)

    if var.MOVIES in (3, 9): # Grimmy's movies
        log.logger("PARS_INSTALLING", form="GRIMMY_MOVIES")
        for num in range(1, 8):
            try:
                ExtractFile(getattr(fl, "GRIMMY" + str(num)), "GrimmyMovies")
            except FileNotFoundError:
                continue
        if os.path.isdir(var.BOOTLEG_TEMP + "GrimmyMovies"):
            StripFolder(var.BOOTLEG_TEMP + "GrimmyMovies")
            CopyFolder(var.BOOTLEG_TEMP + "GrimmyMovies", var.FFVII_PATH + "movies")

    if var.MOVIES == 4: # Rumbah's movies
        try:
            FindFile(fl.MOVIE)
            log.logger("PARS_INSTALLING", form="RUMBAH_MOVIES")
            ExtractFile(fl.MOVIE)
            CopyFolder("{0}{1}\\{2}".format(var.BOOTLEG_TEMP, fl.MOVIE, var.RUMBAH_MOVIES), var.FFVII_PATH + "movies")
            log.logger("PARS_COMPLETED", form="RUMBAH_MOVIES")
        except FileNotFoundError:
            CallSkipMod(fl.MOVIE)

    if var.MOVIES in (9, 10): # Enhanced with Leonhart7413
        exists = True
        for num in range(1, 5):
            try:
                FindFile(fl.LEONHARTMOVIES.format(num))
            except FileNotFoundError:
                CallSkipMod(fl.LEONHARTMOVIES)
                exists = False
                break
        if exists:
            log.logger("PARS_INSTALLING", form="LEONHART_MOVIES")
            ExtractFile(fl.LEONHARTMOVIES.format(1), "LeonhartMovies")
            CopyFolder(var.BOOTLEG_TEMP + "LeonhartMovies", var.FFVII_PATH + "movies")
            log.logger("PARS_COMPLETED", form="LEONHART_MOVIES")

    if var.MOVIES == 10: # Enhanced with Leonhart7413 HD Alternate
        try:
            FindFile(fl.LEONHARTOPENING)
            log.logger("PARS_INSTALLING", form="LEONHART_OPENING")
            ExtractFile(fl.LEONHARTOPENING, "LeonhartOpening")
            CopyFolder(var.BOOTLEG_TEMP + "LeonhartOpening", var.FFVII_PATH + "movies")
            log.logger("PARS_COMPLETED", form="LEONHART_OPENING")
        except FileNotFoundError:
            CallSkipMod(fl.LEONHARTOPENING)

        try:
            for num in range(1, 4):
                FindFile(fl.LEONHARTLOGO.format(num))
            log.logger("PARS_INSTALLING", form="LEONHART_LOGO")
            ExtractFile(fl.LEONHARTLOGO.format(1), "LeonhartLogo")
            CopyFolder(var.BOOTLEG_TEMP + "LeonhartLogo", var.FFVII_PATH + "movies")
            log.logger("PARS_COMPLETED", form="LEONHART_LOGO")
        except FileNotFoundError:
            CallSkipMod(fl.LEONHARTLOGO)

    if var.MOVIES == 11: # Bootlegged reworked with PH03N1XFURY
        try:
            FindFile(fl.FMVSFMV)
            log.logger("PARS_INSTALLING", form="FURY_FMVS")
            ExtractFile(fl.FMVSFMV, "FuryFMVs")
            CopyFolder(var.BOOTLEG_TEMP + "FuryFMVs", var.FFVII_PATH + "movies")
            log.logger("PARS_COMPLETED", form="FURY_FMVS")
        except FileNotFoundError:
            CallSkipMod(fl.FMVSFMV)

        try:
            FindFile(fl.FUNERALFMV)
            log.logger("PARS_INSTALLING", form="FUNERAL_FMVS")
            ExtractFile(fl.FUNERALFMV, "FuneralFMV")
            CopyFolder(var.BOOTLEG_TEMP + "FuneralFMV", var.FFVII_PATH + "movies")
            log.logger("PARS_COMPLETED", form="FUNERAL_FMVS")
        except FileNotFoundError:
            CallSkipMod(fl.FUNERALFMV)

def fmv_no_cait():
    ExecuteFile(fl.FMVNOCAIT, "/verysilent")

def retranslated_fmv():
    ExecuteFile(fl.FMVRETRANS, "/verysilent")
