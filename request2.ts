export class RequestOptions {
	url: URL
	body?: string
	credentials?: RequestCredentials
	mode?: RequestMode
	headers: {[k: string]: string}

	constructor(url: URL) {
		this.url = url
		this.headers = {};
	}

	clone() {
		let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this);
		clone.headers = Object.assign({}, this.headers);
		return clone;
	}

	path(path: string) {
		this.url = new URL(path, this.url);
		return this;
	}

	json(data: any) {
		this.body = JSON.stringify(data);
		this.headers['Content-Type'] = 'application/json';
		return this;
	}

	setCredentials(credentials: RequestCredentials) {
		this.credentials = credentials
		return this;
	}

	setMode(mode: RequestMode) {
		this.mode = mode;
		return this;
	}

	setHeader(header: string, value: string) {
		this.headers[header] = value;
		return this;
	}
}

type FetchHandlers<T, R> = {
	[code: number]: (res: Response) => R,
	ok: (data: T) => R,
}

export class Request2 {
	opts: RequestOptions

	constructor(opts: RequestOptions)
	constructor(url: string | URL)
	constructor(optsOrURL: RequestOptions | string | URL) {
		if (optsOrURL instanceof RequestOptions) {
			this.opts = optsOrURL;
		} else {
			this.opts = new RequestOptions(new URL(optsOrURL))
		};
	}

	async fetch<T, R=T>(method: string, handlers?: FetchHandlers<T, R>) {
		let res = await fetch(this.opts.url, {
			method: method,
			body: this.opts.body,
			credentials: this.opts.credentials,
			mode: this.opts.mode,
			headers: this.opts.headers,
		})

		if (res.ok) {
			let data = await res.json() as T;

			if (handlers) {
				return handlers.ok(data);
			} else {
				return data;
			}
		} else if (handlers && res.status in handlers) {
			return handlers[res.status](res);
		} else {
			throw Error(`Server responded with ${res.status}`)
		}
	}

	with(change: (req: RequestOptions) => RequestOptions) {
		return new Request2(change(this.opts.clone()));
	}
}