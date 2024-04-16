const arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

function partition(low,high) {
  const pivot = low;
  const pivotValue = arr[pivot];
  let lt = low; 
  let gt = high;
  let i = low + 1;

  while(i <= gt) {
    console.log(...arr, "|", lt, gt, i)
    if(arr[i] < pivotValue) {
      swap(lt,i)
      i++;
      lt++;
    }
    else if(arr[i] > pivotValue) {
      swap(i,gt)
      gt--;
    }
    else {
      i++;
    }
  }

  return [lt,gt]
}

function swap(i,j) {
  const temp = arr[j];
  arr[j] = arr[i]
  arr[i] = temp;
}

partition(0,10)