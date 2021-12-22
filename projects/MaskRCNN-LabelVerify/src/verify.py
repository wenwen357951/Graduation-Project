from argparser import args
import json
import os


def verify(image_dir):
    print("Start process " + image_dir, end='')
    label_filepath = os.path.join(image_dir, "via_region_data.json")
    if not os.path.exists(label_filepath):
        raise FileNotFoundError("Label JSON file not found in '{}'.".format(image_dir))

    with open(label_filepath, 'r', encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        all_passed = True
        for key in json_data:
            image_name = key.split(".jpg")[0] + ".jpg"
            image_path = os.path.join(image_dir, image_name)
            image_size = int(key.split(".jpg")[1])
            try:
                if not os.path.exists(image_path):
                    all_passed = False
                    raise FileNotFoundError

                if str(os.path.getsize(image_path)) == image_size:
                    all_passed = False
                    raise KeyError

            except FileNotFoundError:
                print("Key:", key, "File Not Found! \n", image_path)

            except KeyError:
                print("Size Error: ", image_name, "Actual:", os.path.getsize(image_name))

        if all_passed:
            print("\r'{}' Pass!! {}".format(image_dir, " "*10))


def main():
    dataset = os.path.abspath(args.dataset)
    for kind in ["train", "val"]:
        image_dir = os.path.join(dataset, kind)
        if not os.path.exists(image_dir):
            raise FileNotFoundError("Dataset not found '{}' images folder.".format(kind))

        verify(image_dir)

    print("Done.")


if __name__ == '__main__':
    main()
