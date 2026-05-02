from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

GOOD_CODE_EXAMPLES = [

    # ── PYTHON: MATH & ALGORITHMS ────────────────────────────────
    '''def calculate_area(radius):
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    import math
    return math.pi * radius * radius''',

    '''def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1''',

    '''def factorial(n):
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)''',

    '''def fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq''',

    '''def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True''',

    '''def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result''',

    '''def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)''',

    '''def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr''',

    '''def gcd(a, b):
    while b:
        a, b = b, a % b
    return a''',

    '''def lcm(a, b):
    from math import gcd
    return abs(a * b) // gcd(a, b)''',

    '''def power(base, exp):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    return base * power(base, exp - 1)''',

    '''def generate_primes(limit):
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]''',

    '''def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result''',

    '''def chunk_list(lst, size):
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i:i+size] for i in range(0, len(lst), size)]''',

    '''def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []''',

    '''def valid_parentheses(s):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for ch in s:
        if ch in "({[":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0''',

    '''def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]''',

    # ── PYTHON: STRINGS ──────────────────────────────────────────
    '''def is_palindrome(s):
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]''',

    '''def count_vowels(text):
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return sum(1 for ch in text.lower() if ch in "aeiou")''',

    '''def words_frequency(text):
    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq''',

    '''def validate_email(email):
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))''',

    '''def compress_string(s):
    if not s:
        return s
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            result.append(s[i-1] + (str(count) if count > 1 else ""))
            count = 1
    result.append(s[-1] + (str(count) if count > 1 else ""))
    return "".join(result)''',

    '''def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())''',

    '''def title_case(sentence):
    return " ".join(word.capitalize() for word in sentence.split())''',

    # ── PYTHON: FILE I/O ─────────────────────────────────────────
    '''def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except IOError as e:
        raise RuntimeError(f"Failed to read: {e}")''',

    '''def load_json(filepath):
    import json
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    except FileNotFoundError:
        return {}''',

    '''def save_json(filepath, data, indent=2):
    import json
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)''',

    '''def append_to_file(filepath, line):
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line + "\n")''',

    # ── PYTHON: OOP ──────────────────────────────────────────────
    '''class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount''',

    '''class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0''',

    '''class Rectangle:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)''',

    '''class Person:
    def __init__(self, name, age):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        self.name = name.strip()
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}."''',

    '''class Calculator:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b''',

    '''class MinStack:
    def __init__(self):
        self._stack = []
        self._min_stack = []

    def push(self, val):
        self._stack.append(val)
        if not self._min_stack or val <= self._min_stack[-1]:
            self._min_stack.append(val)

    def pop(self):
        val = self._stack.pop()
        if val == self._min_stack[-1]:
            self._min_stack.pop()
        return val''',

    # ── PYTHON: VALIDATION ───────────────────────────────────────
    '''def safe_divide(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b''',

    '''def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")
    return age''',

    '''def get_positive_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val > 0:
                return val
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")''',

    '''def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default''',

    '''def clamp(value, min_val, max_val):
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val")
    return max(min_val, min(value, max_val))''',

    # ── PYTHON: FUNCTIONAL / UTILITIES ───────────────────────────
    '''def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper''',

    '''def normalize(values):
    if not values:
        return []
    min_v = min(values)
    max_v = max(values)
    if min_v == max_v:
        return [0.0] * len(values)
    return [(v - min_v) / (max_v - min_v) for v in values]''',

    '''def moving_average(data, window):
    if window <= 0:
        raise ValueError("Window size must be positive")
    return [sum(data[i:i+window]) / window
            for i in range(len(data) - window + 1)]''',

    '''def partition(lst, predicate):
    true_items = [x for x in lst if predicate(x)]
    false_items = [x for x in lst if not predicate(x)]
    return true_items, false_items''',

    '''def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)''',

    '''def frequency_map(items):
    from collections import Counter
    return dict(Counter(items))''',

    '''def transpose(matrix):
    if not matrix:
        return []
    return [[matrix[j][i] for j in range(len(matrix))]
            for i in range(len(matrix[0]))]''',

    '''def remove_none(lst):
    return [x for x in lst if x is not None]''',

    '''def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)''',

    '''def days_between(date1_str, date2_str):
    from datetime import datetime
    fmt = "%Y-%m-%d"
    d1 = datetime.strptime(date1_str, fmt)
    d2 = datetime.strptime(date2_str, fmt)
    return abs((d2 - d1).days)''',

    '''def generate_id(length=8):
    import random, string
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))''',

    '''def deep_copy(obj):
    import copy
    return copy.deepcopy(obj)''',

    '''def zip_dicts(*dicts):
    keys = set().union(*dicts)
    return {k: [d.get(k) for d in dicts] for k in keys}''',

    '''def retry(func, times=3):
    for attempt in range(times):
        try:
            return func()
        except Exception as e:
            if attempt == times - 1:
                raise
            print(f"Attempt {attempt+1} failed. Retrying...")''',

    # ── JAVASCRIPT: GOOD CODE ────────────────────────────────────
    '''function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}''',

    '''function factorial(n) {
    if (n < 0) throw new Error("Factorial undefined for negative numbers");
    if (n === 0) return 1;
    return n * factorial(n - 1);
}''',

    '''function isPrime(n) {
    if (n < 2) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) return false;
    }
    return true;
}''',

    '''function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    return merge(left, right);
}
function merge(left, right) {
    const result = [];
    let i = 0, j = 0;
    while (i < left.length && j < right.length) {
        if (left[i] <= right[j]) result.push(left[i++]);
        else result.push(right[j++]);
    }
    return result.concat(left.slice(i)).concat(right.slice(j));
}''',

    '''class BankAccount {
    constructor(owner, balance = 0) {
        this.owner = owner;
        this._balance = balance;
    }
    get balance() { return this._balance; }
    deposit(amount) {
        if (amount <= 0) throw new Error("Deposit must be positive");
        this._balance += amount;
    }
    withdraw(amount) {
        if (amount > this._balance) throw new Error("Insufficient funds");
        this._balance -= amount;
    }
}''',

    '''function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) return [seen.get(complement), i];
        seen.set(nums[i], i);
    }
    return [];
}''',

    '''function debounce(func, delay) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}''',

    '''async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Fetch failed:", error.message);
        return null;
    }
}''',

    '''function validateEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}''',

    '''function flattenArray(arr) {
    return arr.reduce((flat, item) =>
        Array.isArray(item) ? flat.concat(flattenArray(item)) : flat.concat(item), []);
}''',

    '''function groupBy(array, key) {
    return array.reduce((groups, item) => {
        const group = item[key];
        groups[group] = groups[group] ?? [];
        groups[group].push(item);
        return groups;
    }, {});
}''',

    '''function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) return cache.get(key);
        const result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}''',

    # ── JAVA: GOOD CODE ──────────────────────────────────────────
    '''public class Calculator {
    public int add(int a, int b) { return a + b; }
    public int subtract(int a, int b) { return a - b; }
    public double divide(double a, double b) {
        if (b == 0) throw new ArithmeticException("Division by zero");
        return a / b;
    }
}''',

    '''public static int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}''',

    '''public static boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) return false;
        left++; right--;
    }
    return true;
}''',

    '''public class Stack<T> {
    private ArrayList<T> items = new ArrayList<>();

    public void push(T item) { items.add(item); }

    public T pop() {
        if (isEmpty()) throw new EmptyStackException();
        return items.remove(items.size() - 1);
    }

    public boolean isEmpty() { return items.isEmpty(); }
}''',

    '''public static int fibonacci(int n) {
    if (n < 0) throw new IllegalArgumentException("n must be non-negative");
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}''',

    '''public class BankAccount {
    private String owner;
    private double balance;

    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Amount must be positive");
        this.balance += amount;
    }

    public double getBalance() { return this.balance; }
}''',

    '''public static int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};
}''',

    '''public static boolean isValidParentheses(String s) {
    Stack<Character> stack = new Stack<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') stack.push(c);
        else if (c == ')' && (stack.isEmpty() || stack.pop() != '(')) return false;
        else if (c == ']' && (stack.isEmpty() || stack.pop() != '[')) return false;
        else if (c == '}' && (stack.isEmpty() || stack.pop() != '{')) return false;
    }
    return stack.isEmpty();
}''',

    # ── C++: GOOD CODE ───────────────────────────────────────────
    '''#include <iostream>
#include <vector>
using namespace std;

int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}''',

    '''#include <vector>
#include <algorithm>

int factorial(int n) {
    if (n < 0) throw std::invalid_argument("n must be non-negative");
    if (n == 0) return 1;
    int result = 1;
    for (int i = 1; i <= n; i++) result *= i;
    return result;
}''',

    '''#include <vector>
using namespace std;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1])
                swap(arr[j], arr[j+1]);
        }
    }
}''',

    '''#include <iostream>
#include <stdexcept>

class Stack {
    int arr[100], top = -1;
public:
    void push(int x) {
        if (top >= 99) throw overflow_error("Stack overflow");
        arr[++top] = x;
    }
    int pop() {
        if (top < 0) throw underflow_error("Stack underflow");
        return arr[top--];
    }
    bool isEmpty() { return top < 0; }
};''',

    '''#include <vector>
#include <unordered_map>

vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.count(complement))
            return {seen[complement], i};
        seen[nums[i]] = i;
    }
    return {};
}''',

    '''#include <iostream>
class BankAccount {
    string owner;
    double balance;
public:
    BankAccount(string o, double b) : owner(o), balance(b) {}
    void deposit(double amount) {
        if (amount <= 0) throw invalid_argument("Must be positive");
        balance += amount;
    }
    double getBalance() const { return balance; }
};''',

    '''#include <vector>
#include <algorithm>

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return false;
    return true;
}

vector<int> sieveOfEratosthenes(int limit) {
    vector<bool> sieve(limit+1, true);
    vector<int> primes;
    sieve[0] = sieve[1] = false;
    for (int i = 2; i <= limit; i++)
        if (sieve[i]) {
            primes.push_back(i);
            for (int j = i*i; j <= limit; j += i)
                sieve[j] = false;
        }
    return primes;
}''',

    # ── SQL: GOOD CODE ───────────────────────────────────────────
    '''SELECT student_id, name, grade
FROM students
WHERE grade >= 60
ORDER BY grade DESC
LIMIT 10;''',

    '''SELECT department, COUNT(*) AS employee_count, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;''',

    '''SELECT o.order_id, c.name, o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.total_amount DESC;''',

    '''CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);''',

    '''UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Engineering'
AND performance_rating >= 4;''',

    '''SELECT p.name, SUM(oi.quantity) AS total_sold
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name
ORDER BY total_sold DESC;''',

    '''BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
COMMIT;''',

    '''CREATE INDEX idx_employee_dept ON employees(department);
CREATE INDEX idx_orders_date ON orders(order_date);''',

]

BAD_CODE_EXAMPLES = [

    # ── PYTHON: SECURITY ISSUES ───────────────────────────────────
    '''user_input = input("Enter code: ")
exec(user_input)
print("Executed!")''',

    '''password = "admin123"
secret = "mysecretkey"
api_key = "sk-1234567890abcdef"
token = "bearer_token_xyz"''',

    '''def process(data):
    return eval(data)''',

    '''def run_cmd(cmd):
    import subprocess
    subprocess.run(cmd, shell=True)''',

    '''import pickle
def load_data(path):
    f = open(path, "rb")
    return pickle.load(f)''',

    '''def authenticate(user, password):
    if user == "admin" and password == "password123":
        return True
    return False''',

    '''class Config:
    SECRET = "my_secret_key"
    DB_PASS = "db_password"
    API = "api_key_123"

    def run(self, cmd):
        return exec(cmd)

    def evaluate(self, expr):
        return eval(expr)''',

    '''USER = "admin"
PASS = "password"
HOST = "192.168.1.1"
def connect():
    return exec(f"psql -h {HOST} -U {USER} -p {PASS}")''',

    '''def sql_query(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    exec(query)''',

    # ── PYTHON: EXCEPTION HANDLING BUGS ──────────────────────────
    '''try:
    import secret_module
    password = secret_module.get_password()
    exec(password)
except:
    pass''',

    '''def fetch_data(url):
    try:
        import urllib.request
        return urllib.request.urlopen(url).read()
    except:
        return None''',

    '''def parse_number(s):
    try:
        return int(s)
    except:
        pass''',

    '''def load_config():
    try:
        with open("config.json") as f:
            import json
            return json.load(f)
    except Exception:
        pass''',

    # ── PYTHON: MUTABLE DEFAULTS ──────────────────────────────────
    '''def append_item(item, lst=[]):
    lst.append(item)
    return lst''',

    '''def add_to_dict(key, val, d={}):
    d[key] = val
    return d''',

    '''def bad_default(x, cache={}):
    cache[x] = x * 2
    return cache''',

    # ── PYTHON: ANTI-PATTERNS ─────────────────────────────────────
    '''def check(x):
    if x == True:
        return True
    elif x == False:
        return False
    else:
        return None''',

    '''def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False''',

    '''def get_len(lst):
    count = 0
    for i in range(len(lst)):
        count = count + 1
    return count''',

    '''def bad_type_check(x):
    if type(x) == int:
        return True
    if type(x) == str:
        return True
    return False''',

    '''for i in range(0,10,1):
    for j in range(0,10,1):
        print(str(i)+" "+str(j))''',

    '''print("starting")
x = 1
print("x is", x)
y = 2
print("y is", y)
z = x + y
print("z is", z)
print("done")''',

    '''import os, sys, re, json, csv, math, random, time, datetime
from os import *
from sys import *''',

    # ── PYTHON: PERFORMANCE ISSUES ────────────────────────────────
    '''def slow_fibonacci(n):
    if n <= 1:
        return n
    return slow_fibonacci(n-1) + slow_fibonacci(n-2)

for i in range(1000):
    print(slow_fibonacci(i))''',

    '''def process_all(items):
    i = 0
    while i < len(items):
        j = 0
        while j < len(items):
            k = 0
            while k < len(items):
                print(items[i], items[j], items[k])
                k += 1
            j += 1
        i += 1''',

    '''result = []
for i in range(100):
    for j in range(100):
        for k in range(100):
            result.append(i + j + k)''',

    # ── PYTHON: MISSING VALIDATION ────────────────────────────────
    '''def divide(a, b):
    result = a / b
    return result''',

    '''def get_item(lst, index):
    return lst[index]''',

    '''def calculate_average(numbers):
    return sum(numbers) / len(numbers)''',

    '''def to_number():
    val = input("Enter a number: ")
    return int(val)''',

    '''x = int(input())
y = int(input())
print(x / y)''',

    '''number = input("Enter number: ")
result = number * 2
print(result)''',

    # ── PYTHON: RESOURCE LEAKS ────────────────────────────────────
    '''def read_all(path):
    f = open(path, "r")
    content = f.read()
    return content''',

    '''def write_data(path, data):
    file = open(path, "w")
    file.write(str(data))''',

    # ── PYTHON: GLOBAL STATE / DEAD CODE ─────────────────────────
    '''state = {"user": None, "logged_in": False}

def login(u):
    global state
    state["user"] = u
    state["logged_in"] = True''',

    '''CACHE = {}
def compute(x):
    global CACHE
    if x in CACHE:
        return CACHE[x]
    CACHE[x] = x * x
    return CACHE[x]''',

    '''def dead_code(x):
    return x * 2
    y = x + 1
    z = y * 3
    return z''',

    '''def never_reached():
    return True
    print("this will never print")
    x = 5
    return False''',

    # ── PYTHON: POOR OOP ──────────────────────────────────────────
    '''class GodClass:
    def __init__(self):
        self.db = None; self.cache = {}
        self.users = []; self.products = []
        password = "godclass123"

    def do_everything(self):
        for u in self.users:
            for p in self.products:
                exec(str(u) + str(p))''',

    '''class bad_class:
    def __init__(self):
        self.x = 0; self.y = 0; self.z = 0
    def doStuff(self):
        self.x=1;self.y=2;self.z=3
    def processData(self):
        return eval(str(self.x))''',

    '''class NoValidation:
    def __init__(self, data):
        self.data = data
    def process(self):
        return eval(self.data)
    def execute(self):
        exec(self.data)
        password = "novalidation123"''',

    # ── JAVASCRIPT: BAD CODE ──────────────────────────────────────
    '''var x = 1
var y = 2
var z = x + y
console.log(x)
console.log(y)
console.log(z)''',

    '''function doStuff(a, b, c, d, e, f) {
    if (a == true) {
        if (b == true) {
            if (c == true) {
                eval(d + e + f);
            }
        }
    }
}''',

    '''var password = "admin123";
var apiKey = "sk-abc123xyz";
function login(user) {
    if (user == "admin") {
        eval("doSomething()");
    }
}''',

    '''function fetchUser(id) {
    var result = null;
    try {
        result = callAPI(id);
    } catch(e) {}
    return result;
}''',

    '''var items = [1,2,3,4,5];
for (var i = 0; i < items.length; i++) {
    for (var j = 0; j < items.length; j++) {
        for (var k = 0; k < items.length; k++) {
            console.log(items[i], items[j], items[k]);
        }
    }
}''',

    '''function getData(url) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send();
    eval(xhr.responseText);
}''',

    '''let x = 1;
let y = 2;
let z = x + y;
console.log("x is " + x);
console.log("y is " + y);
console.log("result is " + z);''',

    # ── JAVA: BAD CODE ────────────────────────────────────────────
    '''public class BadExample {
    public static String password = "admin123";
    public static String secret = "mySecretKey";

    public static void main(String[] args) {
        System.out.println(password);
        System.out.println(secret);
    }
}''',

    '''public int divide(int a, int b) {
    return a / b;
}''',

    '''public void process(List items) {
    try {
        for (int i = 0; i < items.size(); i++) {
            System.out.println(items.get(i));
        }
    } catch (Exception e) {
    }
}''',

    '''public class GodClass {
    String db, cache, users, products, orders;
    String password = "godclass123";

    public void doEverything() {
        for (int i = 0; i < 100; i++) {
            for (int j = 0; j < 100; j++) {
                for (int k = 0; k < 100; k++) {
                    System.out.println(i + j + k);
                }
            }
        }
    }
}''',

    '''public String getUser(int id) {
    try {
        return database.find(id);
    } catch (Exception e) {
        return null;
    }
}''',

    # ── C++: BAD CODE ─────────────────────────────────────────────
    '''#include <iostream>
using namespace std;

int divide(int a, int b) {
    return a / b;
}

int main() {
    cout << divide(10, 0) << endl;
}''',

    '''char password[] = "admin123";
char apiKey[] = "sk-secret-key-xyz";

void login(char* user) {
    if (strcmp(user, "admin") == 0)
        system(password);
}''',

    '''void processAll(int* items, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                printf("%d %d %d\n", items[i], items[j], items[k]);
            }
        }
    }
}''',

    '''int* createArray(int size) {
    int* arr = new int[size];
    return arr;
}

void useArray() {
    int* data = createArray(100);
    data[0] = 1;
}''',

    '''#include <iostream>
using namespace std;
int x, y, z;
void calc() {
    x = 1; y = 2; z = x + y;
    cout << x << endl;
    cout << y << endl;
    cout << z << endl;
}''',

    # ── SQL: BAD CODE ─────────────────────────────────────────────
    '''SELECT * FROM users WHERE username = ''' + "'" + '''admin''' + "'" + ''' AND password = ''' + "'" + '''password123''' + "'" + ''';''',

    '''SELECT * FROM orders;
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM employees;''',

    '''SELECT *
FROM employees e, departments d, projects p, tasks t
WHERE e.dept_id = d.id
AND d.project_id = p.id
AND p.task_id = t.id;''',

    '''UPDATE users SET password = 'newpassword123';''',

    '''DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;''',

]


def train_model():
    X_train = GOOD_CODE_EXAMPLES + BAD_CODE_EXAMPLES
    y_train = ([1] * len(GOOD_CODE_EXAMPLES) + [0] * len(BAD_CODE_EXAMPLES))

    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3),
            max_features=3000,
            sublinear_tf=True
        )),
        ('classifier', MultinomialNB(alpha=0.3))
    ])

    model.fit(X_train, y_train)
    return model


print(f"Training ML model on {len(GOOD_CODE_EXAMPLES) + len(BAD_CODE_EXAMPLES)} samples...")
model = train_model()
print("ML model ready!")


def classify_code(code):
    prediction = model.predict([code])[0]
    probability = model.predict_proba([code])[0]
    confidence = max(probability) * 100

    return {
        "quality": "Good Code" if prediction == 1 else "Needs Improvement",
        "confidence": round(confidence, 1),
        "score": round(probability[1] * 100, 1)
    }