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

struct Basic4 {
  virtual int foo(float x);
  virtual int foofoo(float x) = 0;
  int bar() volatile;
  int baz(char a) const;
  double qux (void) volatile const { return 0.0; }
};

namespace a {
    struct Basic5 {
        void foo(float x);
    };
    namespace b {
        struct Basic6 {
            void foo(int x);
            void bar(Basic5& b5);
            Basic6& operator=(const Basic6& other);
        };
    }   
}

