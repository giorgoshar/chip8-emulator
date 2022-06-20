
jmp main
.ascii "Hello"

{
    load v1 2
}

func main {
    load v14 5
    load v6 45
    jmp inf
}

func inf {
    jmp inf
}