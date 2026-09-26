import json
from pathlib import Path
import uuid

addon_name = ""
addon_description = ""
script_version = ""
script_ui_version = ""
addon_mode = ""
use_script = ""

def setting():
    global addon_name, script_version, script_ui_version, addon_description, use_script, addon_mode
    while True:
        print("作るアドオンの種類\n1.ビヘイビアパックのみ\n2.ビヘイビアパックとリソースパック\n半角数字のみの入力をお願いします")
        addon_mode = input("種類：")
        if addon_mode:
            match addon_mode:
                case "1":
                    addon_mode = "bonly"
                    break
                case "2":
                    addon_mode = "bandr"
                    break
                case _:
                    print(f"半角数字以外のものが入力されました：{addon_mode}")
                    continue
        else:
            print("種類は空にできません")
    while True:
        print("ScriptAPIは使用しますか？ y/n")
        use_script = input()
        if use_script:
            match use_script:
                case "y":
                    break
                case "n":
                    break
                case _:
                    print(f"半角英字のみで入力してください：{use_script}")
    while True:
        addon_name = input("アドオン名: ")
        if addon_name:
            break
        else:
            print("アドオン名は空にできません。")
    if use_script == "y":
        while True:
            script_version = input("ScriptAPIのバージョン: ")
            if script_version:
                script_version = script_version.replace(",", ".")
                break
            else:
                print("バージョンが入力されなかったため、2.3.0を使用します")
                script_version = "2.3.0"
        while True:
            script_ui_version = input("ScriptUIのバージョン: ")
            if script_ui_version:
                script_ui_version = script_ui_version.replace(",", ".")
                break
            else:
                print("バージョンが入力されなかったため、2.0.0を使用します")
                script_ui_version = "2.0.0"
    addon_description = input("アドオンの説明: ")
    return

def make_dir(dir_name: str,dir_path: Path) -> bool:
    dir_path = dir_path / dir_name
    if not dir_path.exists():
        dir_path.mkdir()
        return True
    else:
        return False

def make_file(file_name: str, file_path: Path, content: str) -> bool:
    file_path = file_path / file_name
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    else:
        return False

def make_json(file_name: str, file_path: Path, content: dict) -> bool:
    file_path = file_path / file_name
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
        return True
    else:
        return False

def make_manifest_content() -> dict:
    bp_uuid = str(uuid.uuid4())
    rp_uuid = str(uuid.uuid4())
    if use_script == "y" and addon_mode == "bonly":
        manifest_content_bp = {
            "format_version": 2,
            "header": {
                "name": addon_name,
                "description": addon_description,
                "uuid": bp_uuid,
                "version": [
                1,
                0,
                0
                ],
                "min_engine_version": [
                1,
                20,
                0
                ]
            },
            "modules": [
                {
                "type": "script",
                "language": "javascript",
                "uuid": str(uuid.uuid4()),
                "entry": "scripts/main.js",
                "version": [
                    1,
                    0,
                    0
                ]
                },
                {
                "description": addon_description,
                "type": "data",
                "uuid": str(uuid.uuid4()),
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ],
            "dependencies": [
                {
                "module_name": "@minecraft/server",
                "version": script_version
                },
                {
                "module_name": "@minecraft/server-ui",
                "version": script_ui_version
                }
            ],
            "capabilities": [
                "script_eval"
            ]
        }
        return [manifest_content_bp]
    elif use_script == "y" and addon_mode == "bandr":
        manifest_content_bp = {
            "format_version": 2,
            "header": {
                "name": addon_name,
                "description": addon_description,
                "uuid": bp_uuid,
                "version": [
                1,
                0,
                0
                ],
                "min_engine_version": [
                1,
                20,
                0
                ]
            },
            "modules": [
                {
                "type": "script",
                "language": "javascript",
                "uuid": str(uuid.uuid4()),
                "entry": "scripts/main.js",
                "version": [
                    1,
                    0,
                    0
                ]
                },
                {
                "description": addon_description,
                "type": "data",
                "uuid": str(uuid.uuid4()),
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ],
            "dependencies": [
                {
                "uuid": rp_uuid,
                "version": [
                    1,
                    0,
                    0
                ]
                },
                {
                "module_name": "@minecraft/server",
                "version": script_version
                },
                {
                "module_name": "@minecraft/server-ui",
                "version": script_ui_version
                }
            ],
            "capabilities": [
                "script_eval"
            ]
        }
        manifest_content_rp = {
            "format_version": 2,
            "header": {
                "name": addon_name,
                "description": addon_description,
                "uuid": rp_uuid,
                "version": [
                1,
                0,
                0
                ],
                "min_engine_version": [
                1,
                20,
                0
                ]
            },
            "modules": [
                {
                "description": "Resources",
                "type": "resources",
                "uuid": str(uuid.uuid4()),
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ],
            "dependencies": [
                {
                "uuid": bp_uuid,
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ]
        }
        return [manifest_content_bp,manifest_content_rp]
    elif use_script == "n" and addon_mode == "bonly":
        manifest_content_bp = {
            "format_version": 2,
            "header": {
                "name": addon_name,
                "description": addon_description,
                "uuid": bp_uuid,
                "version": [
                1,
                0,
                0
                ],
                "min_engine_version": [
                1,
                20,
                0
                ]
            },
            "modules": [
                {
                "description": addon_description,
                "type": "data",
                "uuid": str(uuid.uuid4()),
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ],
        }
        return [manifest_content_bp]
    elif use_script == "n" and addon_mode == "bandr":
        manifest_content_bp = {
            "format_version": 2,
            "header": {
                "name": addon_name,
                "description": addon_description,
                "uuid": str(uuid.uuid4()),
                "version": [
                1,
                0,
                0
                ],
                "min_engine_version": [
                1,
                20,
                0
                ]
            },
            "modules": [
                {
                "description": addon_description,
                "type": "data",
                "uuid": str(uuid.uuid4()),
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ],
            "dependencies": [
                {
                "uuid": rp_uuid,
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ]
        }
        manifest_content_rp = {
            "format_version": 2,
            "header": {
                "name": addon_name,
                "description": addon_description,
                "uuid": rp_uuid,
                "version": [
                1,
                0,
                0
                ],
                "min_engine_version": [
                1,
                20,
                0
                ]
            },
            "modules": [
                {
                "description": "Resources",
                "type": "resources",
                "uuid": str(uuid.uuid4()),
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ],
            "dependencies": [
                {
                "uuid": bp_uuid,
                "version": [
                    1,
                    0,
                    0
                ]
                }
            ]
        }
        return [manifest_content_bp,manifest_content_rp]

def main():
    setting()
    bp_dir_path = (Path.home()/"AppData"/"Roaming"/"Minecraft Bedrock"/"Users"/"Shared"/"games"/"com.mojang"/"development_behavior_packs")
    rp_dir_path = (Path.home()/"AppData"/"Roaming"/"Minecraft Bedrock"/"Users"/"Shared"/"games"/"com.mojang"/"development_resource_packs")

    json_content = make_manifest_content()

    # つかうビヘイビアパックのみ
    if use_script == "y" and addon_mode == "bonly":
        make_dir(addon_name+"_BP",bp_dir_path)
        make_dir("scripts",(bp_dir_path/(addon_name+"_BP")))
        make_json("manifest.json",(bp_dir_path/(addon_name+"_BP")),json_content[0])
        make_file("main.js",(bp_dir_path/(addon_name+"_BP")/"scripts"),"")
        print("スクリプトを使用するビヘイビアパックを作成しました")
        return

    # 使わないビヘイビアパックのみ
    if use_script == "n" and addon_mode == "bonly":
        make_dir(addon_name+"_BP",bp_dir_path)
        make_dir("scripts",(bp_dir_path/(addon_name+"_BP")))
        make_json("manifest.json",(bp_dir_path/(addon_name+"_BP")),json_content[0])
        make_file("main.js",(bp_dir_path/(addon_name+"_BP")/"scripts"),"")
        print("スクリプトを使用しないビヘイビアパックを作成しました")
        return

    # 使う bandr
    if use_script == "y" and addon_mode == "bandr":
        make_dir(addon_name+"_BP",bp_dir_path)
        make_dir("scripts",(bp_dir_path/(addon_name+"_BP")))
        make_json("manifest.json",(bp_dir_path/(addon_name+"_BP")),json_content[0])
        make_file("main.js",(bp_dir_path/(addon_name+"_BP")/"scripts"),"")

        make_dir(addon_name+"_RP",rp_dir_path)
        make_json("manifest.json",(rp_dir_path/(addon_name+"_RP")),json_content[1])
        make_dir("textures",(rp_dir_path/(addon_name+"_RP")))
        make_dir("texts",(rp_dir_path/(addon_name+"_RP")))
        make_dir("sounds",(rp_dir_path/(addon_name+"_RP")))
        make_dir("models",(rp_dir_path/(addon_name+"_RP")))
        print("スクリプトを使用するビヘイビアパックとリソースパックを作成しました")
        return

    # 使わない bandr
    if use_script == "n" and addon_mode == "bandr":
        make_dir(addon_name+"_BP",bp_dir_path)
        make_json("manifest.json",(bp_dir_path/(addon_name+"_BP")),json_content[0])

        make_dir(addon_name+"_RP",rp_dir_path)
        make_json("manifest.json",(rp_dir_path/(addon_name+"_RP")),json_content[1])
        make_dir("textures",(rp_dir_path/(addon_name+"_RP")))
        make_dir("texts",(rp_dir_path/(addon_name+"_RP")))
        make_dir("sounds",(rp_dir_path/(addon_name+"_RP")))
        make_dir("models",(rp_dir_path/(addon_name+"_RP")))
        print("スクリプトを使用しないビヘイビアパックとリソースパックを作成しました")
        return
        

if __name__ == "__main__":
    main()