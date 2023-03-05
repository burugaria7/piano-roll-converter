import pvkernel


def main():
    print("Hello")
    resolution = (1920, 1080)
    fps = 30
    video = pvkernel.Video(resolution, fps)
    print("World")

    video.props.midi.paths = "..\\sample\\fur_elise.mid"

    # video.props.keyboard.video_path = "your/video/path.mp4"
    # video.props.keyboard.video_start = 1.23  # seconds
    # video.props.keyboard.crop = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]  # put in actual values here

    video.export("video.mp4")

    video.props.blocks_solid.color = (100, 100, 200)


if __name__ == "__main__":
    main()
