package main

import (
	"fmt"
	"image"
	_ "image/jpeg"
	_ "image/png"
	"log"
	"os"

	"github.com/anthonynsimon/bild/transform"
	"golang.org/x/term"

	"github.com/Van-sh/Mini-Projects/Go/ascii-art/filters"
)

const (
	asciiChars      = " `'\",.(){}[]<>:;+*oO0#@"
	asciiCharLength = uint32(len(asciiChars) - 1)
)

func main() {
	if len(os.Args) != 2 {
		log.Fatalln("PLease provide a path to an image")
	}

	inputPath := os.Args[1]

	if input, _ := os.Stat(inputPath); input.IsDir() {
		log.Fatalln("Please provide the path to an image")
	}

	err := generate(inputPath)
	if err != nil {
		log.Fatalln(err)
	}
}

func generate(inputPath string) error {
	imageFile, err := os.Open(inputPath)
	if err != nil {
		return err
	}
	defer imageFile.Close()

	img, _, err := image.Decode(imageFile)
	if err != nil {
		return err
	}

	maxWidth := 1080

	if img.Bounds().Dx() > maxWidth {
		img = transform.Resize(img, maxWidth, img.Bounds().Dy()*maxWidth/img.Bounds().Dx(), transform.Lanczos)
	}

	width, _, _ := term.GetSize(int(os.Stdout.Fd()))

	m := filters.DifferenceOfGaussians(img, 1, 3)
	n := filters.SobelFilter(m)

	img = transform.Resize(img, width, img.Bounds().Dy()*width/img.Bounds().Dx()/2, transform.Lanczos)

	var (
		threshold uint32
		sample    transform.ResampleFilter
	)

	if width > img.Bounds().Dx() {
		threshold = uint32(0x2000)
		sample = transform.Gaussian
	} else {
		threshold = uint32(0xf000)
		sample = transform.NearestNeighbor
	}

	n = transform.Resize(n, width, n.Bounds().Dy()*width/n.Bounds().Dx()/2, sample)

	fmt.Println(imageFile.Name())
	fmt.Println(img.Bounds())

	for y := 0; y < img.Bounds().Dy(); y++ {
		for x := 0; x < img.Bounds().Dx(); x++ {
			pixelString := ""
			if r, g, b, _ := n.At(x, y).RGBA(); r > threshold || b > threshold || g > threshold {
				if r > threshold && g > threshold {
					pixelString += `\`
				} else if r > threshold {
					pixelString += `|`
				} else if g > threshold {
					pixelString += `/`
				} else if b > threshold {
					pixelString += `=`
				}
			} else {
				r, g, b, a := img.At(x, y).RGBA()
				var tmp uint64 = uint64(r*r) + uint64(g*g) + uint64(b*b)
				greyScale := uint32(tmp/3/0xffff) * a / 0xffff
				strIndex := uint32(float64(greyScale) * float64(asciiCharLength) / float64(0xffff))

				pixelString += fmt.Sprintf("%c", asciiChars[strIndex])
			}
			fmt.Print(pixelString)
		}
		fmt.Print("\n")
	}
	return nil
}
