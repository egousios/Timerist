package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"

	"github.com/urfave/cli"
)

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
					fmt.Println(f.Name(), "\t")
				}

				return nil
			},
		},
	}
	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
