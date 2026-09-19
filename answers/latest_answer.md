# Question

Y — @ Building a LeetCode RAG Agen. X | GY keyboard module errorfix-De X > Sleep -LeetCode x + > Ask Gemini - ag xX

<€ > G fA 2% leetcode.com/problems/sleep/description/ x We

» OO ME

p20 MGmal XX CMR © All Bookmarks

€ = JavaScript < > GP @®submt D * % 8 & Oo & & B Premium
© Description | 1 Editorial | — Solutions | ) Submissions a ¢< <> Code
JavaScript v @ Auto ENQOSD
2621. Sleep 6 SI
7}
Easy Companies Q Hint 8
9 1
Given a positive integer millis, write an asynchronous function that sleeps for millis| milliseconds. It can aD | © iste = Bate.mex())
re any value. 11 | * sleep(100).then(() => console.log(Date.now() - t)) // 100
Gee kOe? 7 12 | */
Note that minor deviation from milLis in the actual sleep duration is acceptable.
Example 1:
Saved Ln 1,Col 1

Input: millis = 100

Output: 100 Testcase > Test Result
Explanation: It should return a promise that resolves after 100ms.

let t = Date.now();
sleep(100).then(() => {

console. log(Date.now() — t); // 100
Di

Example 2:
Input: millis = 200

Output: 200
Explanation: It should return a promise that resolves after 200ms.

Hew O46 Ww BY O

=asmMU Et @ 6 a Gove mrsaes ©

# Solution (JavaScript)

**Solution Explanation**

The task is to create an asynchronous function `sleep` that returns a promise which resolves after a given number of milliseconds.  
In JavaScript the built‑in `setTimeout` schedules a callback after a delay. Wrapping it in a `Promise` lets us use the function with `await` or `.then()`.

**Algorithm**
1. Return a new `Promise`.
2. Inside the promise executor, call `setTimeout` with the supplied `millis` and resolve the promise when the timer fires.

The minor deviation allowed by the timer implementation is acceptable, so no extra handling is required.

---

**Reference Implementation (LeetCode style)**

```javascript
var sleep = function(millis) {
    return new Promise(resolve => setTimeout(resolve, millis));
};
```

---

**Complexity Analysis**

- **Time Complexity:** O(1) – the function only creates a timer; the actual waiting time is handled by the event loop.
- **Space Complexity:** O(1) – only a constant‑size promise and timer handle are allocated.
