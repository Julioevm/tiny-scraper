systems = [
    {"name": "A5200", "id": 40, "extensions": ["a52","bin"]},
    {"name": "AMIGA", "id": 64, "extensions": ["adf","dms","zip","lha","lzh","hdf","hdz","hdf","hd","hds","hfe","ipf","uae","adf","dms","zip","lha","lzh","hdf","hdz","hdf","hd","hds","hfe","ipf","uae"]},
    {"name": "ATARIST", "id": 42, "extensions": ["st", "stx", "msa", "dim", "ipf", "ipf", "ctr"]},
    {"name": "CPS1", "id": 6, "extensions": ["zip","chd","ccd"]},
    {"name": "DOS", "id": 135, "extensions": ["zip","7z","rar","exe","com","bat","iso","img","bin"]},
    {"name": "FBNEO", "id": 142, "extensions": ["zip","chd","bin"]},
    {"name": "GB", "id": 9, "extensions": ["gb", "bin"]},
    {"name": "GG", "id": 21, "extensions": ["gg","bin", "sms"]},
    {"name": "LYNX", "id": 28, "extensions": ["lnx","bin"]},
    {"name": "MDCD", "id": 20, "extensions": ["bin","ccd","chd","cue","img","iso","sub","wav"]},
    {"name": "NAOMI", "id": 56, "extensions": ["chd", "bin", "gdi", "raw"]},
    {"name": "NGP", "id": 82, "extensions": ["ngp","ngc","bin"]},
    {"name": "PCE", "id": 105, "extensions": ["pce","cue","ccd","sgx"]},
    {"name": "PICO", "id": 234, "extensions": ["p8", "png"]},
    {"name": "PS", "id": 57, "extensions": ["bin","img","mdf","iso","cue","ccd","pbp","chd","m3u","toc","cbn","sub","ccd"]},
    {"name": "SCUMMVM", "id": 123, "extensions": ["zip","scummvm", "svm"]},
    {"name": "SMS", "id": 2, "extensions": ["sms,bin"]},
    {"name": "VIC20", "id": 0, "extensions": []},
    {"name": "A7800", "id": 0, "extensions": []},
    {"name": "ATOMISWAVE", "id": 53, "extensions": ["chd","bin","gdi"]},
    {"name": "CPS2", "id": 7, "extensions": ["zip","chd","ccd"]},
    {"name": "DREAMCAST", "id": 23, "extensions": ["cdi","gdi","chd","bin","gdi"]},
    {"name": "FC", "id": 3, "extensions": ["nes","fds","unf","unif","nez","nsf","nez"]},
    {"name": "GBA", "id": 12, "extensions": ["gba","bin"]},
    {"name": "GW", "id": 52, "extensions": ["mgw"]},
    {"name": "MAME", "id": 75, "extensions": ["zip","chd","bin"]},
    {"name": "MSX", "id": 113, "extensions": ["rom","dsk","cas","mx1","mx2","col",]},
    {"name": "NDS", "id": 15, "extensions": ["nds","bin"]},
    {"name": "ONS", "id": 0, "extensions": []},
    {"name": "PCECD", "id": 114, "extensions": ["cue","ccd","chd","pce","iso","sgx","ccd"]},
    {"name": "POKE", "id": 211, "extensions": ["min"]},
    {"name": "PSP", "id": 61, "extensions": ["iso","cso","pbp","chd","m3u","toc"]},
    {"name": "SEGA32X", "id": 19, "extensions": [ "32x","smd","md","bin","ccd","cue","img","iso","sub","wav"]},
    {"name": "VARCADE", "id": 0, "extensions": []},
    {"name": "WS", "id": 45, "extensions": ["ws","wsc","bin"]},
    {"name": "A800", "id": 0, "extensions": []},
    {"name": "ATARI", "id": 0, "extensions": []},
    {"name": "C64", "id": 66, "extensions": ["d64","t64","tap","prg","crt","bin", "ark", "c64"]},
    {"name": "CPS3", "id": 8, "extensions": ["zip","chd","ccd"]},
    {"name": "EASYRPG", "id": 0, "extensions": []},
    {"name": "FDS", "id": 0, "extensions": []},
    {"name": "GBC", "id": 10, "extensions": ["gb","gbc","bin"]},
    {"name": "HBMAME", "id": 0, "extensions": []},
    {"name": "MD", "id": 1, "extensions": ["gen","md","smd","bin","sg"]},
    {"name": "N64", "id": 14, "extensions": ["n64", "v64", "z64", "bin"]},
    {"name": "NEOGEO", "id": 0, "extensions": []},
    {"name": "OPENBOR", "id": 214, "extensions": ["pak"]},
    {"name": "PGM2", "id": 0, "extensions": []},
    {"name": "SATURN", "id": 22, "extensions": ["chd","bin","iso","cue","mdf","m3u"]},
    {"name": "SFC", "id": 4, "extensions": ["sfc","smc","fig","swc","mgd", "zip"]},
    {"name": "VB", "id": 11, "extensions": ["vb", "bin", "vboy"]},
]

def get_system_id(system_name: str) -> int:
    for system in systems:
        if system["name"] == system_name:
            return system["id"]
    return -1

def get_system_extension(system_name: str) -> list[str]:
    for system in systems:
        if system["name"] == system_name:
            return system["extensions"]
    return []