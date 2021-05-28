package main
 
import (
	"fmt"
	"strings"
	"bufio"
	"os"
	"strconv"
)
 
func main() {
	file, err := os.Open("nginx_logs")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)

    sum := 0
    for scanner.Scan() {
        if intField, errOfConv := strconv.Atoi(strings.Split(scanner.Text(), " ")[9]); errOfConv == nil {
			sum += intField
		}
    }
	
	fmt.Printf("Total: %d\n", sum)
}
