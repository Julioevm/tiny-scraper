systems = [
    {"name": "A5200", "id": 40, "extensions": ["a52", "bin", "zip"]},
    {
        "name": "AMIGA",
        "id": 64,
        "extensions": [
            "adf",
            "dms",
            "zip",
            "lha",
            "lzh",
            "hdf",
            "hdz",
            "hd",
            "hds",
            "hfe",
            "ipf",
            "uae",
        ],
    },
    {
        "name": "ATARIST",
        "id": 42,
        "extensions": ["st", "stx", "msa", "dim", "ipf", "ctr", "zip"],
    },
    {"name": "CPS1", "id": 6, "extensions": ["zip", "chd", "ccd"]},
    {
        "name": "DOS",
        "id": 135,
        "extensions": ["zip", "7z", "rar", "exe", "com", "bat", "iso", "img", "bin"],
    },
    {"name": "FBNEO", "id": 142, "extensions": ["zip", "chd", "bin"]},
    {"name": "GB", "id": 9, "extensions": ["gb", "bin", "zip"]},
    {"name": "GG", "id": 21, "extensions": ["gg", "bin", "sms", "zip"]},
    {"name": "LYNX", "id": 28, "extensions": ["lnx", "bin", "zip"]},
    {
        "name": "MDCD",
        "id": 20,
        "extensions": ["bin", "ccd", "chd", "cue", "img", "iso", "sub", "wav", "zip"],
    },
    {"name": "NAOMI", "id": 56, "extensions": ["chd", "bin", "gdi", "raw", "zip"]},
    {"name": "NGP", "id": 82, "extensions": ["ngp", "ngc", "bin", "zip"]},
    {"name": "PCE", "id": 105, "extensions": ["pce", "cue", "ccd", "sgx", "zip"]},
    {"name": "PICO", "id": 234, "extensions": ["p8", "png", "zip"]},
    {
        "name": "PS",
        "id": 57,
        "extensions": [
            "bin",
            "img",
            "mdf",
            "iso",
            "cue",
            "ccd",
            "pbp",
            "chd",
            "m3u",
            "toc",
            "cbn",
            "sub",
            "zip",
        ],
    },
    {"name": "SCUMMVM", "id": 123, "extensions": ["zip", "scummvm", "svm"]},
    {"name": "SMS", "id": 2, "extensions": ["sms", "bin", "zip"]},
    {"name": "VIC20", "id": 0, "extensions": ["zip"]},
    {"name": "A7800", "id": 0, "extensions": ["zip"]},
    {"name": "ATOMISWAVE", "id": 53, "extensions": ["chd", "bin", "gdi", "zip"]},
    {"name": "CPS2", "id": 7, "extensions": ["zip", "chd", "ccd"]},
    {"name": "DREAMCAST", "id": 23, "extensions": ["cdi", "gdi", "chd", "bin", "zip"]},
    {
        "name": "FC",
        "id": 3,
        "extensions": ["nes", "fds", "unf", "unif", "nez", "nsf", "zip"],
    },
    {"name": "GBA", "id": 12, "extensions": ["gba", "bin", "zip"]},
    {"name": "GW", "id": 52, "extensions": ["mgw", "zip"]},
    {"name": "MAME", "id": 75, "extensions": ["zip", "chd", "bin"]},
    {
        "name": "MSX",
        "id": 113,
        "extensions": ["rom", "dsk", "cas", "mx1", "mx2", "col", "zip"],
    },
    {"name": "NDS", "id": 15, "extensions": ["nds", "bin", "zip"]},
    {"name": "ONS", "id": 0, "extensions": ["zip"]},
    {
        "name": "PCECD",
        "id": 114,
        "extensions": ["cue", "ccd", "chd", "pce", "iso", "sgx", "zip"],
    },
    {"name": "POKE", "id": 211, "extensions": ["min", "zip"]},
    {
        "name": "PSP",
        "id": 61,
        "extensions": ["iso", "cso", "pbp", "chd", "m3u", "toc", "zip"],
    },
    {
        "name": "SEGA32X",
        "id": 19,
        "extensions": [
            "32x",
            "smd",
            "md",
            "bin",
            "ccd",
            "cue",
            "img",
            "iso",
            "sub",
            "wav",
            "zip",
        ],
    },
    {"name": "VARCADE", "id": 0, "extensions": ["zip"]},
    {"name": "WS", "id": 45, "extensions": ["ws", "wsc", "bin", "zip"]},
    {"name": "A800", "id": 0, "extensions": ["zip"]},
    {"name": "ATARI", "id": 0, "extensions": ["zip"]},
    {
        "name": "C64",
        "id": 66,
        "extensions": ["d64", "t64", "tap", "prg", "crt", "bin", "ark", "c64", "zip"],
    },
    {"name": "CPS3", "id": 8, "extensions": ["zip", "chd", "ccd"]},
    {"name": "EASYRPG", "id": 0, "extensions": ["zip"]},
    {"name": "FDS", "id": 0, "extensions": ["zip"]},
    {"name": "GBC", "id": 10, "extensions": ["gb", "gbc", "bin", "zip"]},
    {"name": "HBMAME", "id": 0, "extensions": ["zip"]},
    {"name": "MD", "id": 1, "extensions": ["gen", "md", "smd", "bin", "sg", "zip"]},
    {"name": "N64", "id": 14, "extensions": ["n64", "v64", "z64", "bin", "zip"]},
    {"name": "NEOGEO", "id": 0, "extensions": ["zip"]},
    {"name": "OPENBOR", "id": 214, "extensions": ["pak", "zip"]},
    {"name": "PGM2", "id": 0, "extensions": ["zip"]},
    {
        "name": "SATURN",
        "id": 22,
        "extensions": ["chd", "bin", "iso", "cue", "mdf", "m3u", "zip"],
    },
    {"name": "SFC", "id": 4, "extensions": ["sfc", "smc", "fig", "swc", "mgd", "zip"]},
    {"name": "VB", "id": 11, "extensions": ["vb", "bin", "vboy", "zip"]},
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
