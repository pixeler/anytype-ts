import * as I from 'Interface';

const GREGORIAN_MONTH_DAYS: { [key: number]: number } = {
	1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
	7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31,
};
const DAY_SECONDS = 86400;

const G_D_M = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];

/**
 * Converts a Gregorian date to Solar Hijri (Jalali).
 */
export function toJalaali (gy: number, gm: number, gd: number): { jy: number, jm: number, jd: number } {
	const gy2 = (gm > 2) ? (gy + 1) : gy;
	let days = 355666 + (365 * gy) + Math.floor((gy2 + 3) / 4) - Math.floor((gy2 + 99) / 100) + Math.floor((gy2 + 399) / 400) + gd + G_D_M[gm - 1];
	let jy = -1595 + (33 * Math.floor(days / 12053));
	days %= 12053;
	jy += 4 * Math.floor(days / 1461);
	days %= 1461;
	if (days > 365) {
		jy += Math.floor((days - 1) / 365);
		days = (days - 1) % 365;
	};
	const jm = (days < 186) ? 1 + Math.floor(days / 31) : 7 + Math.floor((days - 186) / 30);
	const jd = 1 + ((days < 186) ? (days % 31) : ((days - 186) % 30));
	return { jy, jm, jd };
};

/**
 * Converts a Solar Hijri (Jalali) date to Gregorian.
 */
export function toGregorian (jy: number, jm: number, jd: number): { gy: number, gm: number, gd: number } {
	const jy2 = jy + 1595;
	let days = -355668 + (365 * jy2) + Math.floor(jy2 / 33) * 8 + Math.floor(((jy2 % 33) + 3) / 4) + jd + ((jm < 7) ? (jm - 1) * 31 : ((jm - 7) * 30) + 186);
	let gy = 400 * Math.floor(days / 146097);
	days %= 146097;
	if (days > 36524) {
		gy += 100 * Math.floor(--days / 36524);
		days %= 36524;
		if (days >= 365) days++;
	};
	gy += 4 * Math.floor(days / 1461);
	days %= 1461;
	if (days > 365) {
		gy += Math.floor((days - 1) / 365);
		days = (days - 1) % 365;
	};
	const sal_a = [0, 31, ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
	let gm = 0;
	while (gm < 13 && days >= sal_a[gm]) {
		days -= sal_a[gm];
		gm++;
	};
	const gd = days + 1;
	return { gy, gm, gd };
};

const PERSIAN_DIGITS = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
export function toPersianDigits (s: string | number): string {
	if (s === null || s === undefined) {
		return '';
	};
	return String(s).replace(/[0-9]/g, (w) => PERSIAN_DIGITS[Number(w)]);
};

export function fromPersianDigits (s: string): string {
	if (!s) {
		return '';
	};
	return String(s).replace(/[۰-۹]/g, (w) => String(w.charCodeAt(0) - 1776));
};

export const PERSIAN_MONTH_NAMES = [
	'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
	'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
];

const safeTranslate = (key: string, fallback = ''): string => {
	try {
		if (typeof translate === 'function') {
			const res = translate(key);
			if (res && !res.startsWith('⚠️')) {
				return res;
			}
		}
	} catch {
		// ignore
	}
	return fallback;
};

/**
 * Utility class for date and time manipulation, formatting, and calculations.
 * Provides methods for parsing, formatting, and working with dates and times.
 */
class UtilDate {

	/**
	 * Checks whether the Persian (Solar Hijri) calendar is selected.
	 */
	isPersianCalendar (): boolean {
		try {
			return S.Common?.calendarType === 'persian';
		} catch {
			return false;
		};
	};

	/**
	 * Checks whether a given Persian year is a leap year.
	 */
	isPersianLeapYear (jy: number): boolean {
		const g = toGregorian(jy, 12, 30);
		const j = toJalaali(g.gy, g.gm, g.gd);
		return j.jy === jy && j.jm === 12 && j.jd === 30;
	};

	/**
	 * Returns the current time as a Unix timestamp (seconds since epoch).
	 * @returns {number} The current Unix timestamp.
	 */
	now (): number {
		const date = new Date();
		const timestamp = Math.floor(date.getTime() / 1000);

		return timestamp;
	};

	/**
	 * Returns a Unix timestamp for the given date and time components.
	 * @param {number} [y] - Year.
	 * @param {number} [m] - Month (1-12).
	 * @param {number} [d] - Day of month.
	 * @param {number} [h] - Hour.
	 * @param {number} [i] - Minute.
	 * @param {number} [s] - Second.
	 * @returns {number} The Unix timestamp.
	 */
	timestamp (y?: number, m?: number, d?: number, h?: number, i?: number, s?: number): number {
		y = Number(y) || 0;
		m = Number(m) || 0;
		d = Number(d) || 0;
		h = Number(h) || 0;
		i = Number(i) || 0;
		s = Number(s) || 0;

		if (this.isPersianCalendar() && (y >= 1000 && y < 1900)) {
			const g = toGregorian(y, m || 1, d || 1);
			y = g.gy;
			m = g.gm;
			d = g.gd;
		};

		m = m - 1;

		let t: Date = null;

		if ((y >= 0) && (y < 1000)) { 
			t = new Date(y + 1000, m, d, h, i, s, 0);
			t.setUTCFullYear(t.getFullYear() - 1000); 
		} else {
			t = new Date(y, m, d, h, i, s, 0);
		};

		return Math.floor(t.getTime() / 1000);
	};

	/**
	 * Returns the Unix timestamp for the start of today.
	 * @returns {number} The Unix timestamp for today.
	 */
	today () {
		const t = this.now();
		const { d, m, y } = this.getCalendarDateParam(t);

		return this.timestamp(y, m, d);
	};

	/**
	 * Parses a date string into a Unix timestamp, using the specified format.
	 * @param {string} value - The date string to parse.
	 * @param {I.DateFormat} [format] - The date format.
	 * @returns {number} The parsed Unix timestamp.
	 */
	parseDate (value: string, format?: I.DateFormat): number {
		value = fromPersianDigits(String(value || '').replace(/[\u200E\u200F]/g, '')).trim();

		for (let idx = 0; idx < PERSIAN_MONTH_NAMES.length; idx++) {
			const mName = PERSIAN_MONTH_NAMES[idx];
			if (value.includes(mName)) {
				const monthNum = idx + 1;
				const nums = value.replace(mName, ' ').match(/\d+/g);
				if (nums && nums.length >= 2) {
					let num1 = parseInt(nums[0], 10);
					let num2 = parseInt(nums[1], 10);
					let y = num2 > 1000 ? num2 : (num1 > 1000 ? num1 : num2);
					let d = (y === num2) ? num1 : num2;
					let h = nums[2] ? parseInt(nums[2], 10) : 0;
					let i = nums[3] ? parseInt(nums[3], 10) : 0;
					let s = nums[4] ? parseInt(nums[4], 10) : 0;
					return this.timestamp(y, monthNum, d, h, i, s);
				};
			};
		};

		const [ date, time ] = value.split(' ');

		let d: any = 0;
		let m: any = 0;
		let y: any = 0;
		let h: any = 0;
		let i: any = 0;
		let s: any = 0;

		switch (format) {
			case I.DateFormat.ISO: {
				[ y, m, d ] = String(date || '').split(/[.\-\/]/);
				break;
			};

			case I.DateFormat.ShortUS:
			case I.DateFormat.MonthAbbrBeforeDay:
			case I.DateFormat.Long:
			case I.DateFormat.Default: {
				[ m, d, y ] = String(date || '').split(/[.\-\/]/);
				break;
			};

			default: {
				[ d, m, y ] = String(date || '').split(/[.\-\/]/);
				break;
			};
		};

		[ h, i, s ] = String(time || '').split(':');

		y = Number(y) || 0;
		m = Number(m) || 0;
		d = Number(d) || 0;
		h = Number(h) || 0;
		i = Number(i) || 0;
		s = Number(s) || 0;

		if (d > 1000 && y < 1000) {
			const tmp = y;
			y = d;
			d = tmp;
		};

		m = Math.min(12, Math.max(1, m));

		const md = this.getMonthDays(y);
		const maxDays = md[m] || 31;
		d = Math.min(maxDays, Math.max(1, d));
		h = Math.min(24, Math.max(0, h));
		i = Math.min(60, Math.max(0, i));
		s = Math.min(60, Math.max(0, s));

		return this.timestamp(y, m, d, h, i, s);
	};

	/**
	 * Formats a Unix timestamp using the given format string.
	 * @param {string} format - The format string.
	 * @param {number} timestamp - The Unix timestamp.
	 * @returns {string} The formatted date string.
	 */
	date (format: string, timestamp: number) {
		timestamp = Number(timestamp) || 0;

		const d = new Date(timestamp * 1000);
		const isPersian = this.isPersianCalendar();

		let jy = 0;
		let jm = 0;
		let jd = 0;

		if (isPersian) {
			const j = toJalaali(d.getFullYear(), d.getMonth() + 1, d.getDate());
			jy = j.jy;
			jm = j.jm;
			jd = j.jd;
		};

		const pad = (n: number, c: number) => {
			let s = String(n);
			if ((s = s + '').length < c ) {
				++c;
				const m = c - s.length;
				return new Array(m).join('0') + s;
			} else {
				return s;
			};
		};

		const f: any = {
			// Day
			d: () => {
				return pad(f.j(), 2);
			},
			D: () => {
				const t = f.l(); 
				return isPersian ? t.substring(0, 2) : t.substring(0, 3);
			},
			j: () => {
				return isPersian ? jd : d.getDate();
			},
			// Month
			F: () => {
				if (isPersian) {
					return safeTranslate(`persianMonth${f.n()}`, PERSIAN_MONTH_NAMES[f.n() - 1] || '');
				}
				return safeTranslate(`month${f.n()}`);
			},
			m: () => {
				return pad(f.n(), 2);
			},
			M: () => {
				return isPersian ? f.F() : f.F().substring(0, 3);
			},
			n: () => {
				return isPersian ? jm : (d.getMonth() + 1);
			},
			// Year
			Y: () => {
				return isPersian ? jy : d.getFullYear();
			},
			y: () => {
				return (f.Y() + '').slice(2);
			},
			// Time
			a: () => {
				return d.getHours() > 11 ? 'pm' : 'am';
			},
			A: () => {
				return d.getHours() > 11 ? 'PM' : 'AM';
			},
			g: () => {
				return d.getHours() % 12 || 12;
			},
			h: () => {
				return pad(f.g(), 2);
			},
			H: () => {
				return pad(d.getHours(), 2);
			},
			i: () => {
				return pad(d.getMinutes(), 2);
			},
			s: () => {
				return pad(d.getSeconds(), 2);
			},
			w: () => {
				return d.getDay();
			},
			N: () => {
				const w = f.w();
				return w == 0 ? 7 : w;
			},
			l: () => {
				return safeTranslate(`day${f.N()}`);
			},
		};
		return format.replace(/[\\]?([a-zA-Z])/g, (t: string, s: string) => {
			let ret = null;
			if (t != s) {
				ret = s;
			} else 
			if (f[s]) {
				ret = f[s]();
			} else {
				ret = s;
			};
			return ret;
		});
	};

	/**
	 * Returns the date format string for a given I.DateFormat value.
	 * @param {I.DateFormat} v - The date format enum value.
	 * @returns {string} The format string.
	 */
	dateFormat (v: I.DateFormat): string {
		if (this.isPersianCalendar()) {
			switch (v) {
				default:
				case I.DateFormat.Default:				 return 'l، j F Y';
				case I.DateFormat.Long:					 return 'j F Y';
				case I.DateFormat.MonthAbbrBeforeDay:
				case I.DateFormat.MonthAbbrAfterDay:	 return 'j F Y';
				case I.DateFormat.Nordic:				 return 'j F Y';
				case I.DateFormat.Short:				 return 'Y/m/d';
				case I.DateFormat.ShortUS:				 return 'Y/m/d';
				case I.DateFormat.European:				 return 'd/m/Y';
				case I.DateFormat.ISO:					 return 'Y-m-d';
			};
		};

		let f = '';
		switch (v) {
			default:
			case I.DateFormat.MonthAbbrBeforeDay:	 f = 'M d, Y'; break;
			case I.DateFormat.MonthAbbrAfterDay:	 f = 'd M, Y'; break;
			case I.DateFormat.Short:				 f = 'd.m.Y'; break;
			case I.DateFormat.ShortUS:				 f = 'm.d.Y'; break;
			case I.DateFormat.ISO:					 f = 'Y-m-d'; break;
			case I.DateFormat.Long:					 f = 'F j, Y'; break;
			case I.DateFormat.Nordic:				 f = 'j. M Y'; break;
			case I.DateFormat.European:				 f = 'j.m.Y'; break;
			case I.DateFormat.Default:				 f = 'D, M d, Y'; break;
		};
		return f;
	};

	/**
	 * Formats a Unix timestamp using a predefined date format.
	 * @param {I.DateFormat} f - The date format enum value.
	 * @param {number} t - The Unix timestamp.
	 * @returns {string} The formatted date string.
	 */
	dateWithFormat (f: I.DateFormat, t: number): string {
		let str = this.date(this.dateFormat(f), t);
		if (this.isPersianCalendar()) {
			str = '\u200F' + toPersianDigits(str);
		};
		return str;
	};

	/**
	 * Returns the time format string for a given I.TimeFormat value.
	 * @param {I.TimeFormat} v - The time format enum value.
	 * @returns {string} The format string.
	 */
	timeFormat (v: I.TimeFormat, withSeconds?: boolean): string {
		let f = '';
		const s = withSeconds ? ':s' : '';
		switch (v) {
			default:
			case I.TimeFormat.H12:	 f = `g:i${s} A`; break;
			case I.TimeFormat.H24:	 f = `H:i${s}`; break;
		};
		return f;
	};

	/**
	 * Formats a Unix timestamp using a predefined time format.
	 * @param {I.TimeFormat} f - The time format enum value.
	 * @param {number} t - The Unix timestamp.
	 * @returns {string} The formatted time string.
	 */
	timeWithFormat (f: I.TimeFormat, t: number, withSeconds?: boolean): string {
		let str = this.date(this.timeFormat(f, withSeconds), t);
		if (this.isPersianCalendar()) {
			str = '\u200F' + toPersianDigits(str);
		};
		return str;
	};

	/**
	 * Returns a human-readable string for a given day timestamp (e.g., Today, Tomorrow).
	 * @param {any} t - The Unix timestamp.
	 * @returns {string} The day string.
	 */
	dayString (t: any): string {
		t = Number(t) || 0;

		const ct = this.date('d.m.Y', t);
		const time = this.now();
		const day = (typeof J !== 'undefined' && J.Constant?.day) || DAY_SECONDS;

		let ret = '';
		if (ct == this.date('d.m.Y', time)) {
			ret = safeTranslate('commonToday', 'Today');
		} else
		if (ct == this.date('d.m.Y', time + day)) {
			ret = safeTranslate('commonTomorrow', 'Tomorrow');
		} else
		if (ct == this.date('d.m.Y', time - day)) {
			ret = safeTranslate('commonYesterday', 'Yesterday');
		};
		return ret;
	};

	/**
	 * Returns a human-readable string for how long ago a timestamp was.
	 * @param {number} t - The Unix timestamp.
	 * @returns {string} The time ago string.
	 */
	timeAgo (t: number): string {
		if (!t) {
			return '';
		};

		let ret = '';

		if (this.isToday(t)) {
			ret = this.timeWithFormat(I.TimeFormat.H24, t);
		} else
		if (this.dayString(t)) {
			ret = this.dayString(t);
		} else
		if (this.isThisWeek(t)) {
			ret = this.date('l', t);
		} else {
			const { y } = this.getCalendarDateParam(t);
			const year = y != this.getCalendarDateParam(this.now()).y ? `/${y}` : '';

			ret = `${this.date('d', t)}/${this.date('m', t)}${year}`;
		};

		if (this.isPersianCalendar()) {
			ret = '\u200F' + toPersianDigits(ret);
		};

		return ret;
	};

	/**
	 * Returns if given timestamp is today.
	 * @param {number} t - The Unix timestamp.
	 * @returns {boolean}
	 */
	isToday (t: number): boolean {
		const { d, m, y } = this.getCalendarDateParam(t);

		return this.timestamp(y, m, d) == this.today();
	};

	/**
	 * Returns if given timestamp is current week.
	 * @param {number} t - The Unix timestamp.
	 * @returns {boolean}
	 */
	isThisWeek (t: number): boolean {
		const { firstDay } = S.Common;
		const now = new Date(this.now() * 1000);
		const currentDay = now.getDay() === 0 ? 7 : now.getDay();
		const diff = (currentDay - firstDay + 7) % 7;
		const startOfWeek = new Date(now);
		startOfWeek.setDate(now.getDate() - diff);
		startOfWeek.setHours(0, 0, 0, 0);

		return t >= startOfWeek.getTime() / 1000;
	};

	/**
	 * Returns a human-readable duration string for a given number of seconds.
	 * @param {number} t - The duration in seconds.
	 * @returns {string} The duration string.
	 */
	duration (t: number): string {
		if (!t) {
			return '';
		};

		const day = (typeof J !== 'undefined' && J.Constant?.day) || DAY_SECONDS;
		const y = Math.floor(t / (day * 365));

		t -= y * (day * 365);

		const d = Math.floor(t / day);

		t -= d * day;
		const h = Math.floor(t / 3600);

		t -= h * 3600;
		const m = Math.floor(t / 60);

		t -= m * 60;
		const s = t;

		let ret = '';
		if (y > 0) {
			ret = `${y}y`;
		} else
		if (d > 0) {
			ret = `${d}d`;
		} else
		if (h > 0) {
			ret = `${h}h`;
		} else
		if (m > 0) {
			ret = `${m}min`;
		} else
		if (s > 0) {
			ret = `${s}s`;
		};
		return ret;
	};

	/**
	 * Merges the time from one timestamp with the date from another.
	 * @param {number} date - The date timestamp.
	 * @param {number} time - The time timestamp.
	 * @returns {number} The merged Unix timestamp.
	 */
	mergeTimeWithDate (date: number, time: number) {
		const y = Number(this.date('Y', date));
		const m = Number(this.date('n', date));
		const d = Number(this.date('d', date));

		const h = Number(this.date('H', time));
		const i = Number(this.date('i', time));
		const s = Number(this.date('s', time));
		
		return this.timestamp(y, m, d, h, i, s);
	};

	/**
	 * Parses a time string into hour and minute components.
	 * Accepts 24h values (14:30) and 12h values with a meridiem suffix (2:30 PM).
	 * Inputmask placeholders (_) are stripped, so partially typed values simply fail to parse.
	 * @param {string} value - The time string.
	 * @returns {{ h: number, i: number } | null} The parsed components, or null when the value is not a complete valid time.
	 */
	parseTime (value: string): { h: number, i: number } | null {
		const v = String(value || '').replace(/_/g, '').trim();
		const match = v.match(/^(\d{1,2}):(\d{1,2})\s*(am|pm)?$/i);

		if (!match) {
			return null;
		};

		const meridiem = String(match[3] || '').toLowerCase();
		const i = Number(match[2]);

		let h = Number(match[1]);

		if ((i < 0) || (i > 59)) {
			return null;
		};

		if (meridiem) {
			if ((h < 1) || (h > 12)) {
				return null;
			};

			h = h % 12;

			if (meridiem == 'pm') {
				h += 12;
			};
		} else
		if ((h < 0) || (h > 23)) {
			return null;
		};

		return { h, i };
	};

	/**
	 * Applies a time string to the date part of a timestamp, dropping seconds.
	 * @param {number} t - The base Unix timestamp.
	 * @param {string} value - The time string, see parseTime.
	 * @returns {number | null} The new Unix timestamp, or null when the time string is invalid.
	 */
	withTime (t: number, value: string): number | null {
		const time = this.parseTime(value);

		if (!time) {
			return null;
		};

		const { d, m, y } = this.getCalendarDateParam(t);

		return this.timestamp(y, m, d, time.h, time.i, 0);
	};

	/**
	 * Returns the calendar date parameters (day, month, year) for a timestamp.
	 * @param {number} t - The Unix timestamp.
	 * @returns {{ d: number, m: number, y: number }} The date parameters.
	 */
	getCalendarDateParam (t: number) {
		return {
			d: Number(this.date('j', t)),
			m: Number(this.date('n', t)),
			y: Number(this.date('Y', t)),
		};
	};

	/**
	 * Returns the number of days in each month for a given year.
	 * @param {number} y - The year.
	 * @returns {object} The month days mapping.
	 */
	getMonthDays (y: number) {
		if (this.isPersianCalendar()) {
			const isLeap = this.isPersianLeapYear(y);
			return {
				1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31,
				7: 30, 8: 30, 9: 30, 10: 30, 11: 30,
				12: isLeap ? 30 : 29,
			};
		};

		const ret = (typeof J !== 'undefined' && J.Constant?.monthDays) ? {...J.Constant.monthDays} : {...GREGORIAN_MONTH_DAYS};

		// February
		if (this.isLeapYear(y)) {
			ret[2] = 29;
		};

		return ret;
	};

	/**
	 * Returns an array of day objects for the calendar month view.
	 * @param {number} value - The timestamp for the month.
	 * @param {boolean} [noOther] - Whether to exclude days from other months.
	 * @returns {any[]} The array of day objects.
	 */
	getCalendarMonth (value: number, noOther?: boolean) {
		const { firstDay } = S.Common;
		const { m, y } = this.getCalendarDateParam(value);
		const md = this.getMonthDays(y);
		const today = this.today();
		
		let wdf = Number(this.date('N', this.timestamp(y, m, 1)));
		let wdl = Number(this.date('N', this.timestamp(y, m, md[m])));
		let pm = m - 1;
		let nm = m + 1;
		let py = y;
		let ny = y;

		if (pm < 1) {
			pm = 12;
			py = y - 1;
		};

		if (nm > 12) {
			nm = 1;
			ny = y + 1;
		};

		wdf = (wdf - firstDay + 7) % 7; 
		wdl = (wdl - firstDay + 7) % 7;

		let days = [];

		if (!noOther) {
			for (let i = 1; i <= wdf; ++i) {
				days.push({ d: md[pm] - (wdf - i), m: pm, y: py });
			};
		};

		for (let i = 1; i <= md[m]; ++i) {
			days.push({ y, m, d: i });
		};

		if (!noOther) {
			for (let i = 1; i <= (6 - wdl); ++i) {
				days.push({ d: i, m: nm, y: ny });
			};
		};

		const isPersian = this.isPersianCalendar();

		days = days.map(it => {
			const ts = this.timestamp(it.y, it.m, it.d);
			const wd = Number(this.date('N', ts));

			return {
				...it,
				ts,
				wd, 
				isToday: ts == today,
				isWeekend: isPersian ? (wd === 5) : (wd >= 6),
			};
		});

		return days;
	};

	/**
	 * Checks whether a given year is a leap year.
	 * @remarks A given year is considered a leap year, if it's divisible by 4, but not divisible by 100, unless also divisible by 400.
	 * @param {number} year - The year to check.
	 * @returns {boolean} True if the given year is considered a leap year.
	 */
	isLeapYear (year: number): boolean {
		if (year % 4 !== 0) {
			return false;
		};
		if (year % 400 === 0) {
			return true;
		};
		if (year % 100 === 0) {
			return false;
		};
		return true;
	};

	/**
	 * Returns an array of week day objects for the current locale.
	 * @returns {{ id: number, name: string }[]} The week days.
	 */
	getWeekDays (): { id: number, name: string }[] {
		const { firstDay } = S.Common;
		const ret = [];

		for (let i = firstDay; i <= 7; ++i) {
			ret.push({ id: i, name: translate(`day${i}`) });
		};

		for (let i = 1; i < firstDay; ++i) {
			ret.push({ id: i, name: translate(`day${i}`) });
		};

		return ret;
	};

	/**
	 * Returns an array of month objects for the current locale.
	 * @returns {{ id: number, name: string }[]} The months.
	 */
	getMonths (): { id: number, name: string }[] {
		const ret = [];
		const isPersian = this.isPersianCalendar();
		for (let i = 1; i <= 12; ++i) {
			const name = isPersian ?
				safeTranslate(`persianMonth${i}`, PERSIAN_MONTH_NAMES[i - 1] || '') :
				safeTranslate(`month${i}`, '');
			ret.push({ id: i, name });
		};
		return ret;
	};

	/**
	 * Returns an array of year objects for the given range.
	 * @param {number} start - The start year.
	 * @param {number} end - The end year.
	 * @returns {{ id: number, name: string }[]} The years.
	 */
	getYears (start: number, end: number): { id: number, name: any }[] {
		const ret = [];
		const isPersian = this.isPersianCalendar();
		for (let i = start; i <= end; ++i) {
			ret.push({ id: i, name: isPersian ? toPersianDigits(i) : i });
		};
		return ret;
	};

	/**
	 * Returns the date parameters (day, month, year) for a timestamp.
	 * @param {number} t - The Unix timestamp.
	 * @returns {{ d: number, m: number, y: number, h: number, i: number, s: number }} The date parameters.
	 */
	getDateParam (t: number) {
		const [ d, m, y, h, i, s ] = this.date('j,n,Y,H,i,s', t).split(',').map(it => Number(it));
		return { d, m, y, h, i, s };
	};

};

export default new UtilDate();
