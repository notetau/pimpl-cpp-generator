template<typename U=int>
struct Basic1 {
  int foo(float x);
  void bar(int, float y, double);
  void baz(int z=(42));
  double qux (void) { return 0.0; }
  template<typename T, long N>
  T norf(T t);
};

// access check
struct Basic2 {
private:
    int foo();
public:
    void bar();
    int baz(int x);
};

// constructor & operator overloads
struct Basic3 {
    Basic3();
    Basic3(int x);
    Basic3(float x, float y);
    Basic3(const Basic3&);
    Basic3(Basic3&&);
    ~Basic3();
    Basic3& operator=(const Basic3&);
    Basic3& operator=(Basic3&&);
    Basic3 operator +(const Basic3&);
};
