import management

def main():
    mg = management.Management()
    mg.listimages(
        ('..\\OLD\\images\\layer-ILM\\',
        '..\\OLD\\images\\layer-RPE\\')
    )
    print(mg.layersImgs)

if __name__ == "__main__":
    main()