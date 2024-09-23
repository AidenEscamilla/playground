import java.util.Arrays;

class LeetTest{
  static boolean exists(int[] ints, int k) {
    return (Arrays.binarySearch(ints, k) > 0) ? true : false;
}

  public static void main(String []args){
    int[] input = new int[] {-1,0,1,2,3,4,5,6,7};
    System.out.println(LeetTest.exists(input, 7));
  }
};
