package filters

import (
	"image"
	"image/color"
	"math"
)

// gaussianBlur applies a Gaussian blur to an image.
func gaussianBlur(img image.Image, sigma float64) *image.Gray {
	bounds := img.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y

	// Create a new grayscale image to store the result.
	grayImg := image.NewGray(bounds)

	// Calculate the kernel size based on the sigma value.
	kernelSize := int(3*sigma) + 1
	if kernelSize%2 == 0 {
		kernelSize++ // Ensure kernel size is odd
	}

	// Create the Gaussian kernel.
	kernel := make([]float64, kernelSize)
	sum := 0.0
	for i := 0; i < kernelSize; i++ {
		x := float64(i - kernelSize/2)
		kernel[i] = math.Exp(-(x*x)/(2*sigma*sigma)) / (math.Sqrt(2*math.Pi) * sigma)
		sum += kernel[i]
	}

	// Normalize the kernel.
	for i := 0; i < kernelSize; i++ {
		kernel[i] /= sum
	}

	// Apply the Gaussian blur.
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			var blurredValue float64
			for i := 0; i < kernelSize; i++ {
				kx := x + i - kernelSize/2
				if kx < 0 {
					kx = 0
				} else if kx >= width {
					kx = width - 1
				}

				r, _, _, _ := img.At(kx, y).RGBA()
				grayValue := float64(r / 256) // Convert to grayscale intensity
				blurredValue += grayValue * kernel[i]
			}
			grayImg.SetGray(x, y, color.Gray{Y: uint8(blurredValue)})
		}
	}

	// Apply the Gaussian blur vertically
	tempImg := image.NewGray(bounds)
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			var blurredValue float64
			for i := 0; i < kernelSize; i++ {
				ky := y + i - kernelSize/2
				if ky < 0 {
					ky = 0
				} else if ky >= height {
					ky = height - 1
				}

				grayValue := float64(grayImg.GrayAt(x, ky).Y)
				blurredValue += grayValue * kernel[i]
			}
			tempImg.SetGray(x, y, color.Gray{Y: uint8(blurredValue)})
		}
	}

	return tempImg
}

// DifferenceOfGaussians applies the Difference of Gaussians (DoG) filter to an image.
func DifferenceOfGaussians(img image.Image, sigma1, sigma2 float64) *image.Gray {
	// Apply Gaussian blur with sigma1.
	blurred1 := gaussianBlur(img, sigma1)

	// Apply Gaussian blur with sigma2.
	blurred2 := gaussianBlur(img, sigma2)

	// Create a new grayscale image to store the result.
	bounds := img.Bounds()
	dogImg := image.NewGray(bounds)
	width, height := bounds.Max.X, bounds.Max.Y

	// Calculate the difference of the blurred images.
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			val1 := float64(blurred1.GrayAt(x, y).Y)
			val2 := float64(blurred2.GrayAt(x, y).Y)
			diff := val1 - val2

			// Normalize the difference to the range 0-255.  Important!
			diff = diff + 128 // Shift to make values positive
			if diff < 0 {
				diff = 0
			} else if diff > 255 {
				diff = 255
			}

			dogImg.SetGray(x, y, color.Gray{Y: uint8(diff)})
		}
	}

	return dogImg
}

func SobelFilter(img image.Image) *image.RGBA {
	bounds := img.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y

	// Create a new RGBA image to store the colored result.
	rgbaImg := image.NewRGBA(bounds)

	// Define colors for different angles.
	verticalColor := color.RGBA{R: 255, G: 0, B: 0, A: 255}     // Red
	positive45Color := color.RGBA{R: 0, G: 255, B: 0, A: 255}   // Green
	horizontalColor := color.RGBA{R: 0, G: 0, B: 255, A: 255}   // Blue
	negative45Color := color.RGBA{R: 255, G: 255, B: 0, A: 255} // Yellow
	noEdgeColor := color.RGBA{R: 0, G: 0, B: 0, A: 255}         // Black

	// Sobel operator kernels.
	var (
		gx = [3][3]int{
			{-1, 0, 1},
			{-2, 0, 2},
			{-1, 0, 1},
		}
		gy = [3][3]int{
			{-1, -2, -1},
			{0, 0, 0},
			{1, 2, 1},
		}
	)

	// Iterate over the image pixels (excluding the border).
	for y := 1; y < height-1; y++ {
		for x := 1; x < width-1; x++ {
			var (
				sumX int
				sumY int
			)

			// Apply the Sobel operator.
			for i := -1; i <= 1; i++ {
				for j := -1; j <= 1; j++ {
					r, g, b, _ := img.At(x+j, y+i).RGBA()
					grayValue := int((0.299*float64(r) + 0.587*float64(g) + 0.114*float64(b)) / 256)

					sumX += gx[i+1][j+1] * grayValue
					sumY += gy[i+1][j+1] * grayValue
				}
			}

			// Calculate the magnitude and angle of the gradient.
			magnitude := math.Sqrt(float64(sumX*sumX + sumY*sumY))
			angle := math.Atan2(float64(sumY), float64(sumX)) * 180 / math.Pi

			// Determine the color based on the angle.
			var pixelColor color.RGBA
			if magnitude < 100 { // Threshold to avoid noise
				pixelColor = noEdgeColor
			} else {
				// Normalize angle to 0-360 range
				if angle < 0 {
					angle += 180
				}

				// Assign colors based on angle ranges.
				if angle >= 90 - 23 && angle < 90 + 23 {
					pixelColor = horizontalColor // Horizontal (Blue)
				} else if angle >= 45 - 23 && angle < 45 + 23 {
					pixelColor = positive45Color // +45 degrees (Green)
				} else if angle < 0 + 23 || angle >= 180 - 23 {
					pixelColor = verticalColor // Vertical (Red)
				} else {
					pixelColor = negative45Color // -45 degrees (Yellow)
				}
			}

			// Set the pixel color in the output image.
			rgbaImg.SetRGBA(x, y, pixelColor)
		}
	}

	return rgbaImg
}
