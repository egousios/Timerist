package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"

	"github.com/fatih/color"
	"github.com/urfave/cli"
)

func readLines(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func main() {
	app := cli.NewApp()
	app.Name = "Radical"
	app.Usage = "Developing for Timerist"
	app.Version = "0.2.0"
	app.Commands = []*cli.Command{
		{
			Name:    "shout",
			Aliases: []string{"s"},
			Usage:   "Print text to the console",
			Action: func(c *cli.Context) error {
				fmt.Println(c.Args().First())
				return nil
			},
		},
		{
			Name:    "mkfolder",
			Aliases: []string{"mkf"},
			Usage:   "Creates a directory",
			Action: func(c *cli.Context) error {
				os.Mkdir(c.Args().First(), 0755)
				return nil
			},
		},
		{
			Name:    "delfolder",
			Aliases: []string{"delf"},
			Usage:   "Deletes a directory",
			Action: func(c *cli.Context) error {
				os.Remove(c.Args().First())
				return nil
			},
		},
		{
			Name:    "listdir",
			Aliases: []string{"ls"},
			Usage:   "Lists the contents of a directory",
			Action: func(c *cli.Context) error {
				files, err := ioutil.ReadDir(c.Args().First())
				if err != nil {
					log.Fatal(err)
				}

				for _, f := range files {
					color.Yellow(f.Name(), "\t")
				}

				return nil
			},
		},
		{
			Name:    "readfile",
			Aliases: []string{"rf"},
			Usage:   "Reads a file.",
			Action: func(c *cli.Context) error {
				lines, err := readLines(c.Args().First())
				if err != nil {
					log.Fatalf("readLines: %s", err)
				}
				fmt.Printf("Contents of %s :", c.Args().First())
				fmt.Println("\n")
				for _, ln := range lines {
					color.Cyan(ln)
				}
				return nil
			},
		},
		{
			Name:    "path",
			Aliases: []string{"p"},
			Usage:   "Shows the path to timerist_cli.",
			Action: func(c *cli.Context) error {
				color.Magenta(filepath.Abs("."))
				return nil
			},
		},
	}
	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
