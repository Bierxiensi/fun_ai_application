import time
import requests, json

def get_workflow(server, prompt):
    workflow = json.load(open("z_image_turbo_api.json", "r", encoding="utf-8"))

    # workflow["41"]["inputs"]["width"] = 2048
    # workflow["41"]["inputs"]["height"] = 1024
    workflow["45"]["inputs"]["text"] = prompt

    res = requests.post(
        f"{server}/prompt",
        json={"prompt": workflow}
    )
    res.raise_for_status()
    return res.json()["prompt_id"]


def wait_and_download_image(server, prompt_id, save_path):
    while True:
        res = requests.get(
            f"{server}/history/{prompt_id}"
        )
        res.raise_for_status()
        history = res.json()
        if prompt_id not in history:
            time.sleep(0.5)
            continue

        outputs = history[prompt_id].get("outputs", {})
        for _, output in outputs.items():
            if "images" in output:
                image = output["images"][0]
                img_res = requests.get(
                    f"{server}/view",
                    params={
                        "filename": image["filename"],
                        "type": image["type"],
                        "subfolder": image.get("subfolder", "")
                    }
                )
                img_res.raise_for_status()

                with open(save_path, "wb") as f:
                    f.write(img_res.content)

                print(f"✅ image saved: {save_path}")
                return
       
        time.sleep(5)

if __name__ == "__main__":
    server = "http://127.0.0.1:8001"
    prompt="鸣人站在残破的屋顶边缘，身体微微前倾，右手紧握螺旋丸——那枚闪烁着湛蓝电光的能量球正发出嗡嗡的低鸣。他的橙色运动服被风掀起，九尾查克拉形成的金色狐火在身后燃烧，将夜空染成瑰丽的琥珀色。他的眼神锐利如刀，嘴角带着自信的弧度，仿佛下一秒就会如离弦之箭般冲向敌人，用那招闻名忍界的螺旋丸终结一切。"
    prompt_id = get_workflow(server, prompt)
    wait_and_download_image(server, prompt_id, "mingren.png")
