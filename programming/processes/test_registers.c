extern int add(int a, int b);
int
add(int a, int b){
    int c = a + b;
    return c;
}

int
main(int argc, char **argv){
    int a = 45;
    int b = 43;
    int c = add(a,b);
    return 0;
}
