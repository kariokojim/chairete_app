--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:8hsMiORNPIFwaqUjei4OPQ==$uz8hIANxvM3DkXR5VtVgvYFrzNFViGxfJ1xzx76bP5Q=:JnktBQ92sdl+hG+M9qtbWJGHTb4ZN6jkT8SeVj54MIk=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgagent; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA pgagent;


ALTER SCHEMA pgagent OWNER TO postgres;

--
-- Name: SCHEMA pgagent; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA pgagent IS 'pgAgent system tables';


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: pgagent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgagent WITH SCHEMA pgagent;


--
-- Name: EXTENSION pgagent; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgagent IS 'A PostgreSQL job scheduler';


--
-- Data for Name: pga_jobagent; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobagent (jagpid, jaglogintime, jagstation) FROM stdin;
6372	2025-10-25 03:27:47.55891+03	DESKTOP-IH400E9
\.


--
-- Data for Name: pga_jobclass; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobclass (jclid, jclname) FROM stdin;
\.


--
-- Data for Name: pga_job; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_job (jobid, jobjclid, jobname, jobdesc, jobhostagent, jobenabled, jobcreated, jobchanged, jobagentid, jobnextrun, joblastrun) FROM stdin;
\.


--
-- Data for Name: pga_schedule; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_schedule (jscid, jscjobid, jscname, jscdesc, jscenabled, jscstart, jscend, jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths) FROM stdin;
\.


--
-- Data for Name: pga_exception; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_exception (jexid, jexscid, jexdate, jextime) FROM stdin;
\.


--
-- Data for Name: pga_joblog; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_joblog (jlgid, jlgjobid, jlgstatus, jlgstart, jlgduration) FROM stdin;
\.


--
-- Data for Name: pga_jobstep; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobstep (jstid, jstjobid, jstname, jstdesc, jstenabled, jstkind, jstcode, jstconnstr, jstdbname, jstonerror, jscnextrun) FROM stdin;
\.


--
-- Data for Name: pga_jobsteplog; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobsteplog (jslid, jsljlgid, jsljstid, jslstatus, jslresult, jslstart, jslduration, jsloutput) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

--
-- Database "sacco" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: sacco; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE sacco WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Kenya.1252';


ALTER DATABASE sacco OWNER TO postgres;

\connect sacco

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: gl_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gl_accounts (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    account_type character varying(50) NOT NULL,
    balance numeric(12,2)
);


ALTER TABLE public.gl_accounts OWNER TO postgres;

--
-- Name: gl_accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gl_accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gl_accounts_id_seq OWNER TO postgres;

--
-- Name: gl_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gl_accounts_id_seq OWNED BY public.gl_accounts.id;


--
-- Name: loan_payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loan_payments (
    id integer NOT NULL,
    loan_id integer,
    amount numeric(12,2) NOT NULL,
    interest_paid numeric(12,2),
    principal_paid numeric(12,2),
    payment_date timestamp without time zone
);


ALTER TABLE public.loan_payments OWNER TO postgres;

--
-- Name: loan_payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loan_payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loan_payments_id_seq OWNER TO postgres;

--
-- Name: loan_payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loan_payments_id_seq OWNED BY public.loan_payments.id;


--
-- Name: loan_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loan_products (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    interest_rate numeric(5,2) NOT NULL,
    max_term_months integer NOT NULL
);


ALTER TABLE public.loan_products OWNER TO postgres;

--
-- Name: loan_products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loan_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loan_products_id_seq OWNER TO postgres;

--
-- Name: loan_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loan_products_id_seq OWNED BY public.loan_products.id;


--
-- Name: loans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loans (
    id integer NOT NULL,
    member_id integer,
    loan_product_id integer,
    principal numeric(12,2) NOT NULL,
    interest_rate numeric(5,2) NOT NULL,
    term_months integer NOT NULL,
    status character varying(20),
    date_applied timestamp without time zone,
    date_approved timestamp without time zone,
    date_disbursed timestamp without time zone
);


ALTER TABLE public.loans OWNER TO postgres;

--
-- Name: loans_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loans_id_seq OWNER TO postgres;

--
-- Name: loans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loans_id_seq OWNED BY public.loans.id;


--
-- Name: member_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member_accounts (
    member_id integer NOT NULL,
    savings_balance numeric(12,2),
    share_capital_balance numeric(12,2),
    total_loan_balance numeric(12,2),
    total_interest_due numeric(12,2)
);


ALTER TABLE public.member_accounts OWNER TO postgres;

--
-- Name: members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.members (
    id integer NOT NULL,
    member_number character varying(10) NOT NULL,
    full_name character varying(100) NOT NULL,
    phone character varying(20),
    email character varying(100),
    date_joined timestamp without time zone
);


ALTER TABLE public.members OWNER TO postgres;

--
-- Name: members_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_id_seq OWNER TO postgres;

--
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- Name: savings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.savings (
    id integer NOT NULL,
    member_id integer,
    amount numeric(12,2) NOT NULL,
    date timestamp without time zone,
    description text,
    gl_account_id integer
);


ALTER TABLE public.savings OWNER TO postgres;

--
-- Name: savings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.savings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.savings_id_seq OWNER TO postgres;

--
-- Name: savings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.savings_id_seq OWNED BY public.savings.id;


--
-- Name: share_capital; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.share_capital (
    id integer NOT NULL,
    member_id integer,
    amount numeric(12,2) NOT NULL,
    date timestamp without time zone,
    description text,
    gl_account_id integer
);


ALTER TABLE public.share_capital OWNER TO postgres;

--
-- Name: share_capital_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.share_capital_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.share_capital_id_seq OWNER TO postgres;

--
-- Name: share_capital_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.share_capital_id_seq OWNED BY public.share_capital.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    member_id integer,
    gl_account_id integer,
    amount numeric(12,2) NOT NULL,
    transaction_type character varying(10) NOT NULL,
    date timestamp without time zone,
    description text
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transactions_id_seq OWNER TO postgres;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: gl_accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_accounts ALTER COLUMN id SET DEFAULT nextval('public.gl_accounts_id_seq'::regclass);


--
-- Name: loan_payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_payments ALTER COLUMN id SET DEFAULT nextval('public.loan_payments_id_seq'::regclass);


--
-- Name: loan_products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_products ALTER COLUMN id SET DEFAULT nextval('public.loan_products_id_seq'::regclass);


--
-- Name: loans id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans ALTER COLUMN id SET DEFAULT nextval('public.loans_id_seq'::regclass);


--
-- Name: members id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- Name: savings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings ALTER COLUMN id SET DEFAULT nextval('public.savings_id_seq'::regclass);


--
-- Name: share_capital id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.share_capital ALTER COLUMN id SET DEFAULT nextval('public.share_capital_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Data for Name: gl_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gl_accounts (id, name, account_type, balance) FROM stdin;
1	Cash on Hand	1000	0.00
2	Savings Payable	2000	0.00
3	Loan Appraisal Fee	asset	0.00
4	Loan interest income	income	0.00
5	Sacco Savings	asset	150000.00
6	Member Savings	liability	150000.00
\.


--
-- Data for Name: loan_payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loan_payments (id, loan_id, amount, interest_paid, principal_paid, payment_date) FROM stdin;
\.


--
-- Data for Name: loan_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loan_products (id, name, interest_rate, max_term_months) FROM stdin;
\.


--
-- Data for Name: loans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loans (id, member_id, loan_product_id, principal, interest_rate, term_months, status, date_applied, date_approved, date_disbursed) FROM stdin;
\.


--
-- Data for Name: member_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.member_accounts (member_id, savings_balance, share_capital_balance, total_loan_balance, total_interest_due) FROM stdin;
1	0.00	0.00	0.00	0.00
2	0.00	0.00	0.00	0.00
3	0.00	0.00	0.00	0.00
4	0.00	0.00	0.00	0.00
5	0.00	0.00	0.00	0.00
6	0.00	0.00	0.00	0.00
7	0.00	0.00	0.00	0.00
8	0.00	0.00	0.00	0.00
9	0.00	0.00	0.00	0.00
10	0.00	0.00	0.00	0.00
11	0.00	0.00	0.00	0.00
12	0.00	0.00	0.00	0.00
13	0.00	0.00	0.00	0.00
15	0.00	0.00	0.00	0.00
14	150000.00	0.00	0.00	0.00
16	0.00	0.00	0.00	0.00
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.members (id, member_number, full_name, phone, email, date_joined) FROM stdin;
1	692765	James Muiruri Kariokoo	0721313527	kariokojim@gmail.com	2025-05-31 11:59:25.927404
2	692794	James Muiruri Kariokoo	0721313527	kariokojim@gmail.com	2025-05-31 11:59:54.029946
3	693602	James Muiruri Kariokoo	0721313527	kariokonim@gmail.com	2025-05-31 12:13:22.91426
4	694961	James Muiruri 	1234567	kariokojim@gmail.com	2025-05-31 12:36:01.975006
5	695198	James Muiruri 	6886868	wanjikumuiruri2012@gmail.com	2025-05-31 12:39:58.219059
6	705734	rahab wanjiku	0721313527	jmuiruri@gmail.com	2025-05-31 15:35:35.043821
7	705769	James Mwangi kkk	1234578890	wanjikumuiruri2012@gmail.com	2025-05-31 15:36:09.67382
8	706051	James Mwangi kkk	0721313527	Kariokojim@gmail.com	2025-05-31 15:40:51.538457
9	851298	James Mwangi 656	57575585885	kariokonim@gmail.com	2025-06-02 08:01:38.4911
10	852449	rahab wanjiku	0721313527	wanjikumuiruri2012@gmail.com	2025-06-02 08:20:49.459756
11	852495	rahab wanjiku	0721313527	Kariokojim@gmail.com	2025-06-02 08:21:35.163544
12	852510	rahab wanjiku	0721313527	Kariokojim@gmail.com	2025-06-02 08:21:50.56551
13	852673	rahab wanjiku	0721313527	wanjikumuiruri2012@gmail.com	2025-06-02 08:24:33.975495
14	852712	Andy Gitau Muiruri	0738313527	agitau@gmail.com	2025-06-02 08:25:12.201405
15	064132	rahab wanjiku ggg	123456789909	changa@rocketmail.com	2025-06-04 19:08:52.213168
16	381238	Alvin Kariokoo	0721313527	akmuiruri@gmail.com	2025-06-08 11:13:58.098603
\.


--
-- Data for Name: savings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.savings (id, member_id, amount, date, description, gl_account_id) FROM stdin;
1	14	500.00	2025-06-04 18:27:05.063563	ecdftt	\N
2	1	1000.00	2025-06-04 19:13:35.3048	dggdg	\N
3	1	100000.00	2025-06-04 19:20:45.510984	savings	\N
4	10	40000.00	2025-06-04 19:22:17.138678	savings	\N
5	9	20000.00	2025-06-04 19:24:15.687962	data	\N
6	15	100000000.00	2025-06-07 17:43:34.730877	super save	\N
10	4	5000.00	2025-06-07 19:55:15.849129	savings	\N
11	14	23001.00	2025-06-07 19:55:53.761314	first save	\N
12	14	50000.00	2025-06-07 20:10:04.460267	teeet	\N
13	14	50000.00	2025-06-07 20:12:06.979488	teeet	\N
14	14	50000.00	2025-06-07 20:12:22.701374	teeet	\N
\.


--
-- Data for Name: share_capital; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.share_capital (id, member_id, amount, date, description, gl_account_id) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transactions (id, member_id, gl_account_id, amount, transaction_type, date, description) FROM stdin;
1	\N	1	5000.00	debit	2025-06-07 19:55:15.862065	Saving by member #4
2	\N	2	5000.00	credit	2025-06-07 19:55:15.862073	Saving by member #4
3	\N	1	23001.00	debit	2025-06-07 19:55:53.764203	Saving by member #14
4	\N	2	23001.00	credit	2025-06-07 19:55:53.764208	Saving by member #14
5	14	5	50000.00	debit	2025-06-07 20:10:04.487097	Member saving received
6	14	6	50000.00	credit	2025-06-07 20:10:04.487104	Credit to member savings
7	14	5	50000.00	debit	2025-06-07 20:12:06.99512	Member saving received
8	14	6	50000.00	credit	2025-06-07 20:12:06.995126	Credit to member savings
9	14	5	50000.00	debit	2025-06-07 20:12:22.711429	Member saving received
10	14	6	50000.00	credit	2025-06-07 20:12:22.711437	Credit to member savings
\.


--
-- Name: gl_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gl_accounts_id_seq', 6, true);


--
-- Name: loan_payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loan_payments_id_seq', 1, false);


--
-- Name: loan_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loan_products_id_seq', 1, false);


--
-- Name: loans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loans_id_seq', 1, false);


--
-- Name: members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.members_id_seq', 16, true);


--
-- Name: savings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.savings_id_seq', 19, true);


--
-- Name: share_capital_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.share_capital_id_seq', 1, false);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transactions_id_seq', 10, true);


--
-- Name: gl_accounts gl_accounts_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_accounts
    ADD CONSTRAINT gl_accounts_name_key UNIQUE (name);


--
-- Name: gl_accounts gl_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_accounts
    ADD CONSTRAINT gl_accounts_pkey PRIMARY KEY (id);


--
-- Name: loan_payments loan_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_payments
    ADD CONSTRAINT loan_payments_pkey PRIMARY KEY (id);


--
-- Name: loan_products loan_products_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_products
    ADD CONSTRAINT loan_products_name_key UNIQUE (name);


--
-- Name: loan_products loan_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_products
    ADD CONSTRAINT loan_products_pkey PRIMARY KEY (id);


--
-- Name: loans loans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_pkey PRIMARY KEY (id);


--
-- Name: member_accounts member_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_accounts
    ADD CONSTRAINT member_accounts_pkey PRIMARY KEY (member_id);


--
-- Name: members members_member_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_member_number_key UNIQUE (member_number);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- Name: savings savings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings
    ADD CONSTRAINT savings_pkey PRIMARY KEY (id);


--
-- Name: share_capital share_capital_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.share_capital
    ADD CONSTRAINT share_capital_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: loan_payments loan_payments_loan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_payments
    ADD CONSTRAINT loan_payments_loan_id_fkey FOREIGN KEY (loan_id) REFERENCES public.loans(id);


--
-- Name: loans loans_loan_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_loan_product_id_fkey FOREIGN KEY (loan_product_id) REFERENCES public.loan_products(id);


--
-- Name: loans loans_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- Name: member_accounts member_accounts_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_accounts
    ADD CONSTRAINT member_accounts_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- Name: savings savings_gl_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings
    ADD CONSTRAINT savings_gl_account_id_fkey FOREIGN KEY (gl_account_id) REFERENCES public.gl_accounts(id);


--
-- Name: savings savings_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings
    ADD CONSTRAINT savings_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- Name: share_capital share_capital_gl_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.share_capital
    ADD CONSTRAINT share_capital_gl_account_id_fkey FOREIGN KEY (gl_account_id) REFERENCES public.gl_accounts(id);


--
-- Name: share_capital share_capital_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.share_capital
    ADD CONSTRAINT share_capital_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- Name: transactions transactions_gl_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_gl_account_id_fkey FOREIGN KEY (gl_account_id) REFERENCES public.gl_accounts(id);


--
-- Name: transactions transactions_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- PostgreSQL database dump complete
--

--
-- Database "sacco_db" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: sacco_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE sacco_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Kenya.1252';


ALTER DATABASE sacco_db OWNER TO postgres;

\connect sacco_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: gl_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gl_accounts (
    id integer NOT NULL,
    gl_code character varying(20) NOT NULL,
    gl_name character varying(100) NOT NULL,
    account_type character varying(20),
    balance numeric(15,2)
);


ALTER TABLE public.gl_accounts OWNER TO postgres;

--
-- Name: gl_accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gl_accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gl_accounts_id_seq OWNER TO postgres;

--
-- Name: gl_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gl_accounts_id_seq OWNED BY public.gl_accounts.id;


--
-- Name: gl_postings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gl_postings (
    id integer NOT NULL,
    created_at timestamp without time zone,
    account_code character varying(50) NOT NULL,
    debit numeric(18,2) NOT NULL,
    credit numeric(18,2) NOT NULL,
    narration character varying(255)
);


ALTER TABLE public.gl_postings OWNER TO postgres;

--
-- Name: gl_postings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gl_postings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gl_postings_id_seq OWNER TO postgres;

--
-- Name: gl_postings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gl_postings_id_seq OWNED BY public.gl_postings.id;


--
-- Name: gl_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gl_transactions (
    id integer NOT NULL,
    txn_no character varying(30) NOT NULL,
    gl_code character varying(20) NOT NULL,
    amount numeric(15,2) NOT NULL,
    tran_type character varying(10) NOT NULL,
    narration character varying(100),
    created_at timestamp without time zone,
    posted_by character varying(50) NOT NULL
);


ALTER TABLE public.gl_transactions OWNER TO postgres;

--
-- Name: gl_transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gl_transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gl_transactions_id_seq OWNER TO postgres;

--
-- Name: gl_transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gl_transactions_id_seq OWNED BY public.gl_transactions.id;


--
-- Name: loan_guarantors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loan_guarantors (
    id integer NOT NULL,
    guarantor_no character varying(20),
    amount_guaranteed numeric(12,2),
    member_no character varying(20),
    loan_no character varying(20)
);


ALTER TABLE public.loan_guarantors OWNER TO postgres;

--
-- Name: loan_guarantors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loan_guarantors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loan_guarantors_id_seq OWNER TO postgres;

--
-- Name: loan_guarantors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loan_guarantors_id_seq OWNED BY public.loan_guarantors.id;


--
-- Name: loan_interest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loan_interest (
    id integer NOT NULL,
    month character varying(7),
    interest_due numeric(12,2),
    interest_paid numeric(12,2),
    date_posted timestamp without time zone,
    loan_no character varying(20),
    interest_account character varying(20) DEFAULT 'M000GL_LN_INT'::character varying NOT NULL
);


ALTER TABLE public.loan_interest OWNER TO postgres;

--
-- Name: loan_interest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loan_interest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loan_interest_id_seq OWNER TO postgres;

--
-- Name: loan_interest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loan_interest_id_seq OWNED BY public.loan_interest.id;


--
-- Name: loan_schedules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loan_schedules (
    id integer NOT NULL,
    due_date date,
    principal_due numeric(12,2),
    interest_due numeric(12,2),
    principal_paid numeric(12,2),
    interest_paid numeric(12,2),
    status character varying(20),
    loan_no character varying(20),
    installment_no integer,
    principal_balance numeric(12,2),
    member_no character varying(20)
);


ALTER TABLE public.loan_schedules OWNER TO postgres;

--
-- Name: loan_schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loan_schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loan_schedules_id_seq OWNER TO postgres;

--
-- Name: loan_schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loan_schedules_id_seq OWNED BY public.loan_schedules.id;


--
-- Name: loans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loans (
    id integer NOT NULL,
    status character varying(20),
    loan_no character varying(20) NOT NULL,
    member_no character varying(20),
    loan_account character varying(20) NOT NULL,
    interest_account character varying(20) NOT NULL,
    interest_rate numeric(5,2),
    disbursed_date date,
    created_at timestamp without time zone,
    loan_amount numeric(12,2),
    loan_period integer,
    balance numeric(12,2),
    disbursed_by integer,
    interest_balance numeric(12,2),
    loan_type character varying(20)
);


ALTER TABLE public.loans OWNER TO postgres;

--
-- Name: loans_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loans_id_seq OWNER TO postgres;

--
-- Name: loans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loans_id_seq OWNED BY public.loans.id;


--
-- Name: members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.members (
    id integer NOT NULL,
    member_no character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    phone character varying(20),
    email character varying(120),
    joined_date date,
    dob date,
    id_no character varying(20),
    congregation character varying(100),
    gender character varying(20),
    created_by integer
);


ALTER TABLE public.members OWNER TO postgres;

--
-- Name: members_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_id_seq OWNER TO postgres;

--
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- Name: sacco_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sacco_accounts (
    account_id integer NOT NULL,
    member_no character varying(10) NOT NULL,
    account_number character varying(20) NOT NULL,
    account_type character varying(20) NOT NULL,
    balance numeric(15,2),
    "limit" numeric(15,2),
    status character varying(15),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying(50) NOT NULL
);


ALTER TABLE public.sacco_accounts OWNER TO postgres;

--
-- Name: sacco_accounts_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sacco_accounts_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sacco_accounts_account_id_seq OWNER TO postgres;

--
-- Name: sacco_accounts_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sacco_accounts_account_id_seq OWNED BY public.sacco_accounts.account_id;


--
-- Name: savings_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.savings_accounts (
    id integer NOT NULL,
    member_id integer NOT NULL,
    balance numeric(18,2) NOT NULL
);


ALTER TABLE public.savings_accounts OWNER TO postgres;

--
-- Name: savings_accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.savings_accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.savings_accounts_id_seq OWNER TO postgres;

--
-- Name: savings_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.savings_accounts_id_seq OWNED BY public.savings_accounts.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    created_at timestamp without time zone,
    txn_no character varying(30) NOT NULL,
    member_no character varying(20),
    account_no character varying(20),
    gl_account character varying(20),
    running_balance numeric(15,2),
    reference character varying(50),
    narration character varying(100),
    bank_txn_date date NOT NULL,
    tran_type character varying(10) NOT NULL,
    posted_by character varying(50) NOT NULL,
    debit_amount numeric(15,2) NOT NULL,
    credit_amount numeric(15,2) NOT NULL
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transactions_id_seq OWNER TO postgres;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    email character varying(255),
    password_hash character varying(255) NOT NULL,
    role character varying(50) NOT NULL,
    member_id integer,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: gl_accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_accounts ALTER COLUMN id SET DEFAULT nextval('public.gl_accounts_id_seq'::regclass);


--
-- Name: gl_postings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_postings ALTER COLUMN id SET DEFAULT nextval('public.gl_postings_id_seq'::regclass);


--
-- Name: gl_transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_transactions ALTER COLUMN id SET DEFAULT nextval('public.gl_transactions_id_seq'::regclass);


--
-- Name: loan_guarantors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_guarantors ALTER COLUMN id SET DEFAULT nextval('public.loan_guarantors_id_seq'::regclass);


--
-- Name: loan_interest id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_interest ALTER COLUMN id SET DEFAULT nextval('public.loan_interest_id_seq'::regclass);


--
-- Name: loan_schedules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_schedules ALTER COLUMN id SET DEFAULT nextval('public.loan_schedules_id_seq'::regclass);


--
-- Name: loans id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans ALTER COLUMN id SET DEFAULT nextval('public.loans_id_seq'::regclass);


--
-- Name: members id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- Name: sacco_accounts account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sacco_accounts ALTER COLUMN account_id SET DEFAULT nextval('public.sacco_accounts_account_id_seq'::regclass);


--
-- Name: savings_accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings_accounts ALTER COLUMN id SET DEFAULT nextval('public.savings_accounts_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
b9ae7c328172
\.


--
-- Data for Name: gl_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gl_accounts (id, gl_code, gl_name, account_type, balance) FROM stdin;
1	BANK	Bank Account	Asset	0.00
2	SAVINGS	Member Savings	Liability	0.00
\.


--
-- Data for Name: gl_postings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gl_postings (id, created_at, account_code, debit, credit, narration) FROM stdin;
\.


--
-- Data for Name: gl_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gl_transactions (id, txn_no, gl_code, amount, tran_type, narration, created_at, posted_by) FROM stdin;
3	TXN20251014223020991	SAVINGS	6000.00	DR	Savings deposit by M0001: sep deposit	2025-10-14 22:30:29.4822	admin
4	TXN20251014223020991	BANK	6000.00	CR	Savings deposit by M0001: sep deposit	2025-10-14 22:30:29.482326	admin
5	TXN20251017080045910	SAVINGS	600.00	DR	Savings deposit by M0001: sep deposit	2025-10-17 08:01:34.934163	admin
6	TXN20251017080045910	BANK	600.00	CR	Savings deposit by M0001: sep deposit	2025-10-17 08:01:34.934211	admin
7	TXN20251017081125527894	SAVINGS	50000.00	DR	Savings deposit by M0001: fgggg	2025-10-17 08:11:39.45072	admin
8	TXN20251017081125527894	BANK	50000.00	CR	Savings deposit by M0001: fgggg	2025-10-17 08:11:39.450782	admin
9	TXN20251017082459920860	SAVINGS	700.00	DR	Savings deposit by M0001: sep deposit	2025-10-17 08:25:09.083609	admin
10	TXN20251017082459920371	BANK	700.00	CR	Savings deposit by M0001: sep deposit	2025-10-17 08:25:09.083787	admin
11	TXN21685A87A1	SAVINGS	6000.00	DR	Savings deposit by M0001: sep deposit	2025-10-17 08:28:12.272089	admin
12	TXN21685A87A1	BANK	6000.00	CR	Savings deposit by M0001: sep deposit	2025-10-17 08:28:12.272185	admin
13	TXN907153EB69	SAVINGS	800.00	DR	Savings deposit by M0001: oct deposit	2025-10-17 08:34:33.174975	admin
14	TXN907153EB69	BANK	800.00	CR	Savings deposit by M0001: oct deposit	2025-10-17 08:34:33.175037	admin
15	TXNA58DEB47AD	SAVINGS	888.00	DR	Savings deposit by M0001: oct deposit	2025-10-17 08:34:46.17421	admin
16	TXNA58DEB47AD	BANK	888.00	CR	Savings deposit by M0001: oct deposit	2025-10-17 08:34:46.174256	admin
17	TXN525DEED5FE	SAVINGS	7500.00	DR	Savings deposit by M0001: oct deposit	2025-10-17 08:36:46.674628	admin
18	TXN525DEED5FE	BANK	7500.00	CR	Savings deposit by M0001: oct deposit	2025-10-17 08:36:46.674686	admin
19	TXN32EFE31926	SAVINGS	3333.00	DR	Savings deposit by M0001: oct deposit	2025-10-17 10:34:25.274322	admin
20	TXN32EFE31926	BANK	3333.00	CR	Savings deposit by M0001: oct deposit	2025-10-17 10:34:25.274471	admin
21	TXN8FE21EB36F	SAVINGS	3333.00	DR	Savings deposit by M0001: oct deposit	2025-10-17 10:43:07.275797	admin
22	TXN8FE21EB36F	BANK	3333.00	CR	Savings deposit by M0001: oct deposit	2025-10-17 10:43:07.27598	admin
23	TXN1E4505A21C	SAVINGS	3333.00	DR	Savings deposit by M0001: oct deposit	2025-10-17 10:43:11.562548	admin
24	TXN1E4505A21C	BANK	3333.00	CR	Savings deposit by M0001: oct deposit	2025-10-17 10:43:11.56262	admin
25	TXN6F7A0F4D13	SAVINGS	20000.00	DR	Savings deposit by M0002: sep deposit	2025-10-17 13:02:42.504681	admin
26	TXN6F7A0F4D13	BANK	20000.00	CR	Savings deposit by M0002: sep deposit	2025-10-17 13:02:42.504796	admin
27	TXNFBE7B39991	SAVINGS	50000.00	DR	Savings deposit by M0003: oct deposit	2025-10-17 13:03:24.710006	admin
28	TXNFBE7B39991	BANK	50000.00	CR	Savings deposit by M0003: oct deposit	2025-10-17 13:03:24.71009	admin
29	TXNB78BF21425	SAVINGS	55000.00	DR	Savings deposit by M0002: sep deposit	2025-10-17 13:03:52.415828	admin
30	TXNB78BF21425	BANK	55000.00	CR	Savings deposit by M0002: sep deposit	2025-10-17 13:03:52.416056	admin
31	TXN4000719605	SAVINGS	80000.00	DR	Savings deposit by M0004: sep deposit	2025-10-17 13:04:41.678024	admin
32	TXN4000719605	BANK	80000.00	CR	Savings deposit by M0004: sep deposit	2025-10-17 13:04:41.678124	admin
33	TXN925B6641B9	SAVINGS	20000.00	DR	Savings deposit by M0004: Oct Deposit	2025-10-17 13:05:19.421324	admin
34	TXN925B6641B9	BANK	20000.00	CR	Savings deposit by M0004: Oct Deposit	2025-10-17 13:05:19.421467	admin
\.


--
-- Data for Name: loan_guarantors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loan_guarantors (id, guarantor_no, amount_guaranteed, member_no, loan_no) FROM stdin;
\.


--
-- Data for Name: loan_interest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loan_interest (id, month, interest_due, interest_paid, date_posted, loan_no, interest_account) FROM stdin;
\.


--
-- Data for Name: loan_schedules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loan_schedules (id, due_date, principal_due, interest_due, principal_paid, interest_paid, status, loan_no, installment_no, principal_balance, member_no) FROM stdin;
708	2025-09-30	11482.05	1681.25	0.00	0.00	DUE	LN0002	1	123017.95	M0009
709	2025-10-30	11625.57	1537.72	0.00	0.00	DUE	LN0002	2	111392.38	M0009
710	2025-11-30	11770.89	1392.40	0.00	0.00	DUE	LN0002	3	99621.48	M0009
711	2025-12-30	11918.03	1245.27	0.00	0.00	DUE	LN0002	4	87703.45	M0009
712	2026-01-30	12067.01	1096.29	0.00	0.00	DUE	LN0002	5	75636.45	M0009
713	2026-02-28	12217.84	945.46	0.00	0.00	DUE	LN0002	6	63418.60	M0009
714	2026-03-28	12370.57	792.73	0.00	0.00	DUE	LN0002	7	51048.04	M0009
715	2026-04-28	12525.20	638.10	0.00	0.00	DUE	LN0002	8	38522.84	M0009
716	2026-05-28	12681.76	481.54	0.00	0.00	DUE	LN0002	9	25841.07	M0009
717	2026-06-28	12840.29	323.01	0.00	0.00	DUE	LN0002	10	13000.79	M0009
718	2026-07-28	13000.79	162.51	0.00	0.00	DUE	LN0002	11	0.00	M0009
719	2025-09-30	6122.59	2126.69	0.00	0.00	DUE	LN0003	1	164012.41	M0010
720	2025-10-30	6199.12	2050.16	0.00	0.00	DUE	LN0003	2	157813.29	M0010
721	2025-11-30	6276.61	1972.67	0.00	0.00	DUE	LN0003	3	151536.68	M0010
722	2025-12-30	6355.07	1894.21	0.00	0.00	DUE	LN0003	4	145181.61	M0010
723	2026-01-30	6434.51	1814.77	0.00	0.00	DUE	LN0003	5	138747.11	M0010
724	2026-02-28	6514.94	1734.34	0.00	0.00	DUE	LN0003	6	132232.17	M0010
725	2026-03-28	6596.37	1652.90	0.00	0.00	DUE	LN0003	7	125635.80	M0010
726	2026-04-28	6678.83	1570.45	0.00	0.00	DUE	LN0003	8	118956.97	M0010
727	2026-05-28	6762.31	1486.96	0.00	0.00	DUE	LN0003	9	112194.66	M0010
728	2026-06-28	6846.84	1402.43	0.00	0.00	DUE	LN0003	10	105347.81	M0010
729	2026-07-28	6932.43	1316.85	0.00	0.00	DUE	LN0003	11	98415.38	M0010
730	2026-08-28	7019.08	1230.19	0.00	0.00	DUE	LN0003	12	91396.30	M0010
731	2026-09-28	7106.82	1142.45	0.00	0.00	DUE	LN0003	13	84289.48	M0010
732	2026-10-28	7195.66	1053.62	0.00	0.00	DUE	LN0003	14	77093.82	M0010
733	2026-11-28	7285.60	963.67	0.00	0.00	DUE	LN0003	15	69808.22	M0010
734	2026-12-28	7376.67	872.60	0.00	0.00	DUE	LN0003	16	62431.55	M0010
735	2027-01-28	7468.88	780.39	0.00	0.00	DUE	LN0003	17	54962.66	M0010
736	2027-02-28	7562.24	687.03	0.00	0.00	DUE	LN0003	18	47400.42	M0010
737	2027-03-28	7656.77	592.51	0.00	0.00	DUE	LN0003	19	39743.65	M0010
738	2027-04-28	7752.48	496.80	0.00	0.00	DUE	LN0003	20	31991.17	M0010
739	2027-05-28	7849.39	399.89	0.00	0.00	DUE	LN0003	21	24141.78	M0010
740	2027-06-28	7947.50	301.77	0.00	0.00	DUE	LN0003	22	16194.28	M0010
741	2027-07-28	8046.85	202.43	0.00	0.00	DUE	LN0003	23	8147.43	M0010
742	2027-08-28	8147.43	101.84	0.00	0.00	DUE	LN0003	24	0.00	M0010
743	2025-09-30	6465.65	2245.85	0.00	0.00	DUE	LN0004	1	173202.35	M0011
744	2025-10-30	6546.47	2165.03	0.00	0.00	DUE	LN0004	2	166655.88	M0011
745	2025-11-30	6628.30	2083.20	0.00	0.00	DUE	LN0004	3	160027.58	M0011
746	2025-12-30	6711.15	2000.34	0.00	0.00	DUE	LN0004	4	153316.43	M0011
747	2026-01-30	6795.04	1916.46	0.00	0.00	DUE	LN0004	5	146521.38	M0011
748	2026-02-28	6879.98	1831.52	0.00	0.00	DUE	LN0004	6	139641.40	M0011
749	2026-03-28	6965.98	1745.52	0.00	0.00	DUE	LN0004	7	132675.42	M0011
750	2026-04-28	7053.06	1658.44	0.00	0.00	DUE	LN0004	8	125622.36	M0011
751	2026-05-28	7141.22	1570.28	0.00	0.00	DUE	LN0004	9	118481.14	M0011
752	2026-06-28	7230.48	1481.01	0.00	0.00	DUE	LN0004	10	111250.66	M0011
753	2026-07-28	7320.87	1390.63	0.00	0.00	DUE	LN0004	11	103929.79	M0011
754	2026-08-28	7412.38	1299.12	0.00	0.00	DUE	LN0004	12	96517.42	M0011
755	2026-09-28	7505.03	1206.47	0.00	0.00	DUE	LN0004	13	89012.38	M0011
756	2026-10-28	7598.84	1112.65	0.00	0.00	DUE	LN0004	14	81413.54	M0011
757	2026-11-28	7693.83	1017.67	0.00	0.00	DUE	LN0004	15	73719.71	M0011
758	2026-12-28	7790.00	921.50	0.00	0.00	DUE	LN0004	16	65929.71	M0011
759	2027-01-28	7887.38	824.12	0.00	0.00	DUE	LN0004	17	58042.33	M0011
760	2027-02-28	7985.97	725.53	0.00	0.00	DUE	LN0004	18	50056.36	M0011
761	2027-03-28	8085.79	625.70	0.00	0.00	DUE	LN0004	19	41970.57	M0011
762	2027-04-28	8186.87	524.63	0.00	0.00	DUE	LN0004	20	33783.70	M0011
763	2027-05-28	8289.20	422.30	0.00	0.00	DUE	LN0004	21	25494.50	M0011
764	2027-06-28	8392.82	318.68	0.00	0.00	DUE	LN0004	22	17101.68	M0011
765	2027-07-28	8497.73	213.77	0.00	0.00	DUE	LN0004	23	8603.95	M0011
766	2027-08-28	8603.95	107.55	0.00	0.00	DUE	LN0004	24	0.00	M0011
767	2025-09-30	11430.17	1352.10	0.00	0.00	DUE	LN0005	1	96737.83	M0022
768	2025-10-30	11573.05	1209.22	0.00	0.00	DUE	LN0005	2	85164.78	M0022
769	2025-11-30	11717.71	1064.56	0.00	0.00	DUE	LN0005	3	73447.06	M0022
770	2025-12-30	11864.18	918.09	0.00	0.00	DUE	LN0005	4	61582.88	M0022
771	2026-01-30	12012.49	769.79	0.00	0.00	DUE	LN0005	5	49570.39	M0022
772	2026-02-28	12162.64	619.63	0.00	0.00	DUE	LN0005	6	37407.75	M0022
773	2026-03-28	12314.68	467.60	0.00	0.00	DUE	LN0005	7	25093.08	M0022
774	2026-04-28	12468.61	313.66	0.00	0.00	DUE	LN0005	8	12624.47	M0022
775	2026-05-28	12624.47	157.81	0.00	0.00	DUE	LN0005	9	0.00	M0022
776	2025-09-30	3989.76	2250.00	0.00	0.00	DUE	LN0006	1	176010.24	M0023
777	2025-10-30	4039.63	2200.13	0.00	0.00	DUE	LN0006	2	171970.61	M0023
778	2025-11-30	4090.13	2149.63	0.00	0.00	DUE	LN0006	3	167880.48	M0023
779	2025-12-30	4141.25	2098.51	0.00	0.00	DUE	LN0006	4	163739.23	M0023
780	2026-01-30	4193.02	2046.74	0.00	0.00	DUE	LN0006	5	159546.21	M0023
781	2026-02-28	4245.43	1994.33	0.00	0.00	DUE	LN0006	6	155300.78	M0023
782	2026-03-28	4298.50	1941.26	0.00	0.00	DUE	LN0006	7	151002.28	M0023
783	2026-04-28	4352.23	1887.53	0.00	0.00	DUE	LN0006	8	146650.05	M0023
784	2026-05-28	4406.63	1833.13	0.00	0.00	DUE	LN0006	9	142243.42	M0023
785	2026-06-28	4461.72	1778.04	0.00	0.00	DUE	LN0006	10	137781.70	M0023
786	2026-07-28	4517.49	1722.27	0.00	0.00	DUE	LN0006	11	133264.21	M0023
787	2026-08-28	4573.96	1665.80	0.00	0.00	DUE	LN0006	12	128690.26	M0023
788	2026-09-28	4631.13	1608.63	0.00	0.00	DUE	LN0006	13	124059.12	M0023
789	2026-10-28	4689.02	1550.74	0.00	0.00	DUE	LN0006	14	119370.10	M0023
790	2026-11-28	4747.63	1492.13	0.00	0.00	DUE	LN0006	15	114622.47	M0023
791	2026-12-28	4806.98	1432.78	0.00	0.00	DUE	LN0006	16	109815.49	M0023
792	2027-01-28	4867.07	1372.69	0.00	0.00	DUE	LN0006	17	104948.43	M0023
793	2027-02-28	4927.90	1311.86	0.00	0.00	DUE	LN0006	18	100020.52	M0023
794	2027-03-28	4989.50	1250.26	0.00	0.00	DUE	LN0006	19	95031.02	M0023
795	2027-04-28	5051.87	1187.89	0.00	0.00	DUE	LN0006	20	89979.15	M0023
796	2027-05-28	5115.02	1124.74	0.00	0.00	DUE	LN0006	21	84864.13	M0023
797	2027-06-28	5178.96	1060.80	0.00	0.00	DUE	LN0006	22	79685.17	M0023
798	2027-07-28	5243.69	996.06	0.00	0.00	DUE	LN0006	23	74441.48	M0023
799	2027-08-28	5309.24	930.52	0.00	0.00	DUE	LN0006	24	69132.24	M0023
800	2027-09-28	5375.61	864.15	0.00	0.00	DUE	LN0006	25	63756.63	M0023
801	2027-10-28	5442.80	796.96	0.00	0.00	DUE	LN0006	26	58313.83	M0023
802	2027-11-28	5510.84	728.92	0.00	0.00	DUE	LN0006	27	52802.99	M0023
803	2027-12-28	5579.72	660.04	0.00	0.00	DUE	LN0006	28	47223.27	M0023
804	2028-01-28	5649.47	590.29	0.00	0.00	DUE	LN0006	29	41573.80	M0023
805	2028-02-28	5720.09	519.67	0.00	0.00	DUE	LN0006	30	35853.72	M0023
806	2028-03-28	5791.59	448.17	0.00	0.00	DUE	LN0006	31	30062.13	M0023
807	2028-04-28	5863.98	375.78	0.00	0.00	DUE	LN0006	32	24198.15	M0023
808	2028-05-28	5937.28	302.48	0.00	0.00	DUE	LN0006	33	18260.87	M0023
809	2028-06-28	6011.50	228.26	0.00	0.00	DUE	LN0006	34	12249.37	M0023
810	2028-07-28	6086.64	153.12	0.00	0.00	DUE	LN0006	35	6162.73	M0023
811	2028-08-28	6162.73	77.03	0.00	0.00	DUE	LN0006	36	0.00	M0023
812	2025-09-30	9784.32	4776.02	0.00	0.00	DUE	LN0007	1	372297.68	M0027
813	2025-10-30	9906.62	4653.72	0.00	0.00	DUE	LN0007	2	362391.06	M0027
814	2025-11-30	10030.46	4529.89	0.00	0.00	DUE	LN0007	3	352360.60	M0027
815	2025-12-30	10155.84	4404.51	0.00	0.00	DUE	LN0007	4	342204.76	M0027
816	2026-01-30	10282.79	4277.56	0.00	0.00	DUE	LN0007	5	331921.98	M0027
817	2026-02-28	10411.32	4149.02	0.00	0.00	DUE	LN0007	6	321510.66	M0027
818	2026-03-28	10541.46	4018.88	0.00	0.00	DUE	LN0007	7	310969.20	M0027
819	2026-04-28	10673.23	3887.11	0.00	0.00	DUE	LN0007	8	300295.97	M0027
820	2026-05-28	10806.65	3753.70	0.00	0.00	DUE	LN0007	9	289489.32	M0027
821	2026-06-28	10941.73	3618.62	0.00	0.00	DUE	LN0007	10	278547.59	M0027
822	2026-07-28	11078.50	3481.84	0.00	0.00	DUE	LN0007	11	267469.09	M0027
823	2026-08-28	11216.98	3343.36	0.00	0.00	DUE	LN0007	12	256252.11	M0027
824	2026-09-28	11357.19	3203.15	0.00	0.00	DUE	LN0007	13	244894.92	M0027
825	2026-10-28	11499.16	3061.19	0.00	0.00	DUE	LN0007	14	233395.76	M0027
826	2026-11-28	11642.90	2917.45	0.00	0.00	DUE	LN0007	15	221752.86	M0027
827	2026-12-28	11788.43	2771.91	0.00	0.00	DUE	LN0007	16	209964.43	M0027
828	2027-01-28	11935.79	2624.56	0.00	0.00	DUE	LN0007	17	198028.64	M0027
829	2027-02-28	12084.99	2475.36	0.00	0.00	DUE	LN0007	18	185943.65	M0027
830	2027-03-28	12236.05	2324.30	0.00	0.00	DUE	LN0007	19	173707.60	M0027
831	2027-04-28	12389.00	2171.35	0.00	0.00	DUE	LN0007	20	161318.60	M0027
832	2027-05-28	12543.86	2016.48	0.00	0.00	DUE	LN0007	21	148774.74	M0027
833	2027-06-28	12700.66	1859.68	0.00	0.00	DUE	LN0007	22	136074.08	M0027
834	2027-07-28	12859.42	1700.93	0.00	0.00	DUE	LN0007	23	123214.66	M0027
835	2027-08-28	13020.16	1540.18	0.00	0.00	DUE	LN0007	24	110194.50	M0027
836	2027-09-28	13182.91	1377.43	0.00	0.00	DUE	LN0007	25	97011.59	M0027
837	2027-10-28	13347.70	1212.64	0.00	0.00	DUE	LN0007	26	83663.89	M0027
838	2027-11-28	13514.55	1045.80	0.00	0.00	DUE	LN0007	27	70149.34	M0027
839	2027-12-28	13683.48	876.87	0.00	0.00	DUE	LN0007	28	56465.86	M0027
840	2028-01-28	13854.52	705.82	0.00	0.00	DUE	LN0007	29	42611.34	M0027
841	2028-02-28	14027.70	532.64	0.00	0.00	DUE	LN0007	30	28583.64	M0027
842	2028-03-28	14203.05	357.30	0.00	0.00	DUE	LN0007	31	14380.59	M0027
843	2028-04-28	14380.59	179.76	0.00	0.00	DUE	LN0007	32	0.00	M0027
844	2025-09-30	24974.86	9521.55	0.00	0.00	DUE	LN0008	1	736749.14	M0051
845	2025-10-30	25287.05	9209.36	0.00	0.00	DUE	LN0008	2	711462.09	M0051
846	2025-11-30	25603.14	8893.28	0.00	0.00	DUE	LN0008	3	685858.95	M0051
847	2025-12-30	25923.18	8573.24	0.00	0.00	DUE	LN0008	4	659935.78	M0051
848	2026-01-30	26247.21	8249.20	0.00	0.00	DUE	LN0008	5	633688.56	M0051
849	2026-02-28	26575.30	7921.11	0.00	0.00	DUE	LN0008	6	607113.26	M0051
850	2026-03-28	26907.50	7588.92	0.00	0.00	DUE	LN0008	7	580205.76	M0051
851	2026-04-28	27243.84	7252.57	0.00	0.00	DUE	LN0008	8	552961.92	M0051
852	2026-05-28	27584.39	6912.02	0.00	0.00	DUE	LN0008	9	525377.54	M0051
853	2026-06-28	27929.19	6567.22	0.00	0.00	DUE	LN0008	10	497448.34	M0051
854	2026-07-28	28278.31	6218.10	0.00	0.00	DUE	LN0008	11	469170.04	M0051
855	2026-08-28	28631.79	5864.63	0.00	0.00	DUE	LN0008	12	440538.25	M0051
856	2026-09-28	28989.68	5506.73	0.00	0.00	DUE	LN0008	13	411548.56	M0051
857	2026-10-28	29352.05	5144.36	0.00	0.00	DUE	LN0008	14	382196.51	M0051
858	2026-11-28	29718.96	4777.46	0.00	0.00	DUE	LN0008	15	352477.55	M0051
859	2026-12-28	30090.44	4405.97	0.00	0.00	DUE	LN0008	16	322387.11	M0051
860	2027-01-28	30466.57	4029.84	0.00	0.00	DUE	LN0008	17	291920.54	M0051
861	2027-02-28	30847.41	3649.01	0.00	0.00	DUE	LN0008	18	261073.13	M0051
862	2027-03-28	31233.00	3263.41	0.00	0.00	DUE	LN0008	19	229840.14	M0051
863	2027-04-28	31623.41	2873.00	0.00	0.00	DUE	LN0008	20	198216.73	M0051
864	2027-05-28	32018.70	2477.71	0.00	0.00	DUE	LN0008	21	166198.02	M0051
865	2027-06-28	32418.94	2077.48	0.00	0.00	DUE	LN0008	22	133779.09	M0051
866	2027-07-28	32824.17	1672.24	0.00	0.00	DUE	LN0008	23	100954.91	M0051
867	2027-08-28	33234.48	1261.94	0.00	0.00	DUE	LN0008	24	67720.44	M0051
868	2027-09-28	33649.91	846.51	0.00	0.00	DUE	LN0008	25	34070.53	M0051
869	2027-10-28	34070.53	425.88	0.00	0.00	DUE	LN0008	26	0.00	M0051
870	2025-09-30	21362.00	267.02	0.00	0.00	DUE	LN0009	1	0.00	M0054
871	2025-09-30	16497.84	7750.00	0.00	0.00	DUE	LN0010	1	603502.16	M0059
872	2025-10-30	16704.06	7543.78	0.00	0.00	DUE	LN0010	2	586798.10	M0059
873	2025-11-30	16912.86	7334.98	0.00	0.00	DUE	LN0010	3	569885.24	M0059
874	2025-12-30	17124.27	7123.57	0.00	0.00	DUE	LN0010	4	552760.97	M0059
875	2026-01-30	17338.33	6909.51	0.00	0.00	DUE	LN0010	5	535422.64	M0059
876	2026-02-28	17555.05	6692.78	0.00	0.00	DUE	LN0010	6	517867.59	M0059
877	2026-03-28	17774.49	6473.34	0.00	0.00	DUE	LN0010	7	500093.09	M0059
878	2026-04-28	17996.67	6251.16	0.00	0.00	DUE	LN0010	8	482096.42	M0059
879	2026-05-28	18221.63	6026.21	0.00	0.00	DUE	LN0010	9	463874.79	M0059
880	2026-06-28	18449.40	5798.43	0.00	0.00	DUE	LN0010	10	445425.38	M0059
881	2026-07-28	18680.02	5567.82	0.00	0.00	DUE	LN0010	11	426745.36	M0059
882	2026-08-28	18913.52	5334.32	0.00	0.00	DUE	LN0010	12	407831.84	M0059
883	2026-09-28	19149.94	5097.90	0.00	0.00	DUE	LN0010	13	388681.90	M0059
884	2026-10-28	19389.31	4858.52	0.00	0.00	DUE	LN0010	14	369292.59	M0059
885	2026-11-28	19631.68	4616.16	0.00	0.00	DUE	LN0010	15	349660.91	M0059
886	2026-12-28	19877.08	4370.76	0.00	0.00	DUE	LN0010	16	329783.83	M0059
887	2027-01-28	20125.54	4122.30	0.00	0.00	DUE	LN0010	17	309658.29	M0059
888	2027-02-28	20377.11	3870.73	0.00	0.00	DUE	LN0010	18	289281.18	M0059
889	2027-03-28	20631.82	3616.01	0.00	0.00	DUE	LN0010	19	268649.36	M0059
890	2027-04-28	20889.72	3358.12	0.00	0.00	DUE	LN0010	20	247759.64	M0059
891	2027-05-28	21150.84	3097.00	0.00	0.00	DUE	LN0010	21	226608.80	M0059
892	2027-06-28	21415.23	2832.61	0.00	0.00	DUE	LN0010	22	205193.57	M0059
893	2027-07-28	21682.92	2564.92	0.00	0.00	DUE	LN0010	23	183510.65	M0059
894	2027-08-28	21953.95	2293.88	0.00	0.00	DUE	LN0010	24	161556.70	M0059
895	2027-09-28	22228.38	2019.46	0.00	0.00	DUE	LN0010	25	139328.32	M0059
896	2027-10-28	22506.23	1741.60	0.00	0.00	DUE	LN0010	26	116822.08	M0059
897	2027-11-28	22787.56	1460.28	0.00	0.00	DUE	LN0010	27	94034.52	M0059
898	2027-12-28	23072.41	1175.43	0.00	0.00	DUE	LN0010	28	70962.11	M0059
899	2028-01-28	23360.81	887.03	0.00	0.00	DUE	LN0010	29	47601.30	M0059
900	2028-02-28	23652.82	595.02	0.00	0.00	DUE	LN0010	30	23948.48	M0059
901	2028-03-28	23948.48	299.36	0.00	0.00	DUE	LN0010	31	0.00	M0059
902	2025-09-30	11836.04	1565.56	0.00	0.00	DUE	LN0011	1	113408.96	M0063
903	2025-10-30	11983.99	1417.61	0.00	0.00	DUE	LN0011	2	101424.97	M0063
904	2025-11-30	12133.79	1267.81	0.00	0.00	DUE	LN0011	3	89291.19	M0063
905	2025-12-30	12285.46	1116.14	0.00	0.00	DUE	LN0011	4	77005.73	M0063
906	2026-01-30	12439.03	962.57	0.00	0.00	DUE	LN0011	5	64566.70	M0063
907	2026-02-28	12594.52	807.08	0.00	0.00	DUE	LN0011	6	51972.18	M0063
908	2026-03-28	12751.95	649.65	0.00	0.00	DUE	LN0011	7	39220.23	M0063
909	2026-04-28	12911.35	490.25	0.00	0.00	DUE	LN0011	8	26308.89	M0063
910	2026-05-28	13072.74	328.86	0.00	0.00	DUE	LN0011	9	13236.15	M0063
911	2026-06-28	13236.15	165.45	0.00	0.00	DUE	LN0011	10	0.00	M0063
912	2025-09-30	18266.13	9948.39	0.00	0.00	DUE	LN0012	1	777604.87	M0076
913	2025-10-30	18494.45	9720.06	0.00	0.00	DUE	LN0012	2	759110.42	M0076
914	2025-11-30	18725.63	9488.88	0.00	0.00	DUE	LN0012	3	740384.79	M0076
915	2025-12-30	18959.70	9254.81	0.00	0.00	DUE	LN0012	4	721425.08	M0076
916	2026-01-30	19196.70	9017.81	0.00	0.00	DUE	LN0012	5	702228.38	M0076
917	2026-02-28	19436.66	8777.85	0.00	0.00	DUE	LN0012	6	682791.73	M0076
918	2026-03-28	19679.62	8534.90	0.00	0.00	DUE	LN0012	7	663112.11	M0076
919	2026-04-28	19925.61	8288.90	0.00	0.00	DUE	LN0012	8	643186.50	M0076
920	2026-05-28	20174.68	8039.83	0.00	0.00	DUE	LN0012	9	623011.81	M0076
921	2026-06-28	20426.87	7787.65	0.00	0.00	DUE	LN0012	10	602584.95	M0076
922	2026-07-28	20682.20	7532.31	0.00	0.00	DUE	LN0012	11	581902.75	M0076
923	2026-08-28	20940.73	7273.78	0.00	0.00	DUE	LN0012	12	560962.02	M0076
924	2026-09-28	21202.49	7012.03	0.00	0.00	DUE	LN0012	13	539759.53	M0076
925	2026-10-28	21467.52	6746.99	0.00	0.00	DUE	LN0012	14	518292.01	M0076
926	2026-11-28	21735.86	6478.65	0.00	0.00	DUE	LN0012	15	496556.14	M0076
927	2026-12-28	22007.56	6206.95	0.00	0.00	DUE	LN0012	16	474548.58	M0076
928	2027-01-28	22282.66	5931.86	0.00	0.00	DUE	LN0012	17	452265.93	M0076
929	2027-02-28	22561.19	5653.32	0.00	0.00	DUE	LN0012	18	429704.74	M0076
930	2027-03-28	22843.20	5371.31	0.00	0.00	DUE	LN0012	19	406861.53	M0076
931	2027-04-28	23128.74	5085.77	0.00	0.00	DUE	LN0012	20	383732.79	M0076
932	2027-05-28	23417.85	4796.66	0.00	0.00	DUE	LN0012	21	360314.93	M0076
933	2027-06-28	23710.58	4503.94	0.00	0.00	DUE	LN0012	22	336604.36	M0076
934	2027-07-28	24006.96	4207.55	0.00	0.00	DUE	LN0012	23	312597.40	M0076
935	2027-08-28	24307.05	3907.47	0.00	0.00	DUE	LN0012	24	288290.35	M0076
936	2027-09-28	24610.88	3603.63	0.00	0.00	DUE	LN0012	25	263679.47	M0076
937	2027-10-28	24918.52	3295.99	0.00	0.00	DUE	LN0012	26	238760.95	M0076
938	2027-11-28	25230.00	2984.51	0.00	0.00	DUE	LN0012	27	213530.95	M0076
939	2027-12-28	25545.38	2669.14	0.00	0.00	DUE	LN0012	28	187985.57	M0076
940	2028-01-28	25864.69	2349.82	0.00	0.00	DUE	LN0012	29	162120.88	M0076
941	2028-02-28	26188.00	2026.51	0.00	0.00	DUE	LN0012	30	135932.87	M0076
942	2028-03-28	26515.35	1699.16	0.00	0.00	DUE	LN0012	31	109417.52	M0076
943	2028-04-28	26846.79	1367.72	0.00	0.00	DUE	LN0012	32	82570.73	M0076
944	2028-05-28	27182.38	1032.13	0.00	0.00	DUE	LN0012	33	55388.35	M0076
945	2028-06-28	27522.16	692.35	0.00	0.00	DUE	LN0012	34	27866.19	M0076
946	2028-07-28	27866.19	348.33	0.00	0.00	DUE	LN0012	35	0.00	M0076
947	2025-09-30	4997.47	731.75	0.00	0.00	DUE	LN0013	1	53542.53	M0079
948	2025-10-30	5059.93	669.28	0.00	0.00	DUE	LN0013	2	48482.60	M0079
949	2025-11-30	5123.18	606.03	0.00	0.00	DUE	LN0013	3	43359.42	M0079
950	2025-12-30	5187.22	541.99	0.00	0.00	DUE	LN0013	4	38172.19	M0079
951	2026-01-30	5252.06	477.15	0.00	0.00	DUE	LN0013	5	32920.13	M0079
952	2026-02-28	5317.71	411.50	0.00	0.00	DUE	LN0013	6	27602.42	M0079
953	2026-03-28	5384.19	345.03	0.00	0.00	DUE	LN0013	7	22218.23	M0079
954	2026-04-28	5451.49	277.73	0.00	0.00	DUE	LN0013	8	16766.74	M0079
955	2026-05-28	5519.63	209.58	0.00	0.00	DUE	LN0013	9	11247.11	M0079
956	2026-06-28	5588.63	140.59	0.00	0.00	DUE	LN0013	10	5658.48	M0079
957	2026-07-28	5658.48	70.73	0.00	0.00	DUE	LN0013	11	0.00	M0079
958	2025-09-30	16766.11	1983.30	0.00	0.00	DUE	LN0014	1	141897.89	M0123
959	2025-10-30	16975.69	1773.72	0.00	0.00	DUE	LN0014	2	124922.20	M0123
960	2025-11-30	17187.89	1561.53	0.00	0.00	DUE	LN0014	3	107734.31	M0123
961	2025-12-30	17402.73	1346.68	0.00	0.00	DUE	LN0014	4	90331.58	M0123
962	2026-01-30	17620.27	1129.14	0.00	0.00	DUE	LN0014	5	72711.31	M0123
963	2026-02-28	17840.52	908.89	0.00	0.00	DUE	LN0014	6	54870.79	M0123
964	2026-03-28	18063.53	685.88	0.00	0.00	DUE	LN0014	7	36807.26	M0123
965	2026-04-28	18289.32	460.09	0.00	0.00	DUE	LN0014	8	18517.94	M0123
966	2026-05-28	18517.94	231.47	0.00	0.00	DUE	LN0014	9	0.00	M0123
967	2025-09-30	17964.00	224.55	0.00	0.00	DUE	LN0015	1	0.00	M0131
968	2025-09-30	10118.00	126.48	0.00	0.00	DUE	LN0016	1	0.00	M0163
969	2025-09-30	21260.43	8472.51	0.00	0.00	DUE	LN0017	1	656540.57	M0166
970	2025-10-30	21526.18	8206.76	0.00	0.00	DUE	LN0017	2	635014.39	M0166
971	2025-11-30	21795.26	7937.68	0.00	0.00	DUE	LN0017	3	613219.13	M0166
972	2025-12-30	22067.70	7665.24	0.00	0.00	DUE	LN0017	4	591151.43	M0166
973	2026-01-30	22343.55	7389.39	0.00	0.00	DUE	LN0017	5	568807.88	M0166
974	2026-02-28	22622.84	7110.10	0.00	0.00	DUE	LN0017	6	546185.04	M0166
975	2026-03-28	22905.63	6827.31	0.00	0.00	DUE	LN0017	7	523279.41	M0166
976	2026-04-28	23191.95	6540.99	0.00	0.00	DUE	LN0017	8	500087.46	M0166
977	2026-05-28	23481.85	6251.09	0.00	0.00	DUE	LN0017	9	476605.62	M0166
978	2026-06-28	23775.37	5957.57	0.00	0.00	DUE	LN0017	10	452830.25	M0166
979	2026-07-28	24072.56	5660.38	0.00	0.00	DUE	LN0017	11	428757.69	M0166
980	2026-08-28	24373.47	5359.47	0.00	0.00	DUE	LN0017	12	404384.22	M0166
981	2026-09-28	24678.14	5054.80	0.00	0.00	DUE	LN0017	13	379706.08	M0166
982	2026-10-28	24986.61	4746.33	0.00	0.00	DUE	LN0017	14	354719.47	M0166
983	2026-11-28	25298.95	4433.99	0.00	0.00	DUE	LN0017	15	329420.52	M0166
984	2026-12-28	25615.18	4117.76	0.00	0.00	DUE	LN0017	16	303805.34	M0166
985	2027-01-28	25935.37	3797.57	0.00	0.00	DUE	LN0017	17	277869.96	M0166
986	2027-02-28	26259.57	3473.37	0.00	0.00	DUE	LN0017	18	251610.40	M0166
987	2027-03-28	26587.81	3145.13	0.00	0.00	DUE	LN0017	19	225022.59	M0166
988	2027-04-28	26920.16	2812.78	0.00	0.00	DUE	LN0017	20	198102.43	M0166
989	2027-05-28	27256.66	2476.28	0.00	0.00	DUE	LN0017	21	170845.77	M0166
990	2027-06-28	27597.37	2135.57	0.00	0.00	DUE	LN0017	22	143248.40	M0166
991	2027-07-28	27942.34	1790.61	0.00	0.00	DUE	LN0017	23	115306.07	M0166
992	2027-08-28	28291.61	1441.33	0.00	0.00	DUE	LN0017	24	87014.45	M0166
993	2027-09-28	28645.26	1087.68	0.00	0.00	DUE	LN0017	25	58369.19	M0166
994	2027-10-28	29003.33	729.61	0.00	0.00	DUE	LN0017	26	29365.87	M0166
995	2027-11-28	29365.87	367.07	0.00	0.00	DUE	LN0017	27	0.00	M0166
996	2025-09-30	228356.00	2854.45	0.00	0.00	DUE	LN0018	1	0.00	M0168
997	2025-09-30	25765.26	7266.76	0.00	0.00	DUE	LN0019	1	555575.74	M0171
998	2025-10-30	26087.33	6944.70	0.00	0.00	DUE	LN0019	2	529488.41	M0171
999	2025-11-30	26413.42	6618.61	0.00	0.00	DUE	LN0019	3	503075.00	M0171
1000	2025-12-30	26743.58	6288.44	0.00	0.00	DUE	LN0019	4	476331.41	M0171
1001	2026-01-30	27077.88	5954.14	0.00	0.00	DUE	LN0019	5	449253.53	M0171
1002	2026-02-28	27416.35	5615.67	0.00	0.00	DUE	LN0019	6	421837.18	M0171
1003	2026-03-28	27759.06	5272.96	0.00	0.00	DUE	LN0019	7	394078.12	M0171
1004	2026-04-28	28106.05	4925.98	0.00	0.00	DUE	LN0019	8	365972.08	M0171
1005	2026-05-28	28457.37	4574.65	0.00	0.00	DUE	LN0019	9	337514.71	M0171
1006	2026-06-28	28813.09	4218.93	0.00	0.00	DUE	LN0019	10	308701.62	M0171
1007	2026-07-28	29173.25	3858.77	0.00	0.00	DUE	LN0019	11	279528.37	M0171
1008	2026-08-28	29537.92	3494.10	0.00	0.00	DUE	LN0019	12	249990.45	M0171
1009	2026-09-28	29907.14	3124.88	0.00	0.00	DUE	LN0019	13	220083.31	M0171
1010	2026-10-28	30280.98	2751.04	0.00	0.00	DUE	LN0019	14	189802.33	M0171
1011	2026-11-28	30659.49	2372.53	0.00	0.00	DUE	LN0019	15	159142.83	M0171
1012	2026-12-28	31042.74	1989.29	0.00	0.00	DUE	LN0019	16	128100.10	M0171
1013	2027-01-28	31430.77	1601.25	0.00	0.00	DUE	LN0019	17	96669.33	M0171
1014	2027-02-28	31823.66	1208.37	0.00	0.00	DUE	LN0019	18	64845.67	M0171
1015	2027-03-28	32221.45	810.57	0.00	0.00	DUE	LN0019	19	32624.22	M0171
1016	2027-04-28	32624.22	407.80	0.00	0.00	DUE	LN0019	20	0.00	M0171
1017	2025-09-30	13917.00	173.96	0.00	0.00	DUE	LN0020	1	0.00	M0174
1018	2025-09-30	7757.86	4375.00	0.00	0.00	DUE	LN0021	1	342242.14	M0179
1019	2025-10-30	7854.84	4278.03	0.00	0.00	DUE	LN0021	2	334387.30	M0179
1020	2025-11-30	7953.02	4179.84	0.00	0.00	DUE	LN0021	3	326434.27	M0179
1021	2025-12-30	8052.44	4080.43	0.00	0.00	DUE	LN0021	4	318381.84	M0179
1022	2026-01-30	8153.09	3979.77	0.00	0.00	DUE	LN0021	5	310228.74	M0179
1023	2026-02-28	8255.01	3877.86	0.00	0.00	DUE	LN0021	6	301973.74	M0179
1024	2026-03-28	8358.19	3774.67	0.00	0.00	DUE	LN0021	7	293615.55	M0179
1025	2026-04-28	8462.67	3670.19	0.00	0.00	DUE	LN0021	8	285152.87	M0179
1026	2026-05-28	8568.45	3564.41	0.00	0.00	DUE	LN0021	9	276584.42	M0179
1027	2026-06-28	8675.56	3457.31	0.00	0.00	DUE	LN0021	10	267908.86	M0179
1028	2026-07-28	8784.00	3348.86	0.00	0.00	DUE	LN0021	11	259124.86	M0179
1029	2026-08-28	8893.80	3239.06	0.00	0.00	DUE	LN0021	12	250231.05	M0179
1030	2026-09-28	9004.98	3127.89	0.00	0.00	DUE	LN0021	13	241226.08	M0179
1031	2026-10-28	9117.54	3015.33	0.00	0.00	DUE	LN0021	14	232108.54	M0179
1032	2026-11-28	9231.51	2901.36	0.00	0.00	DUE	LN0021	15	222877.03	M0179
1033	2026-12-28	9346.90	2785.96	0.00	0.00	DUE	LN0021	16	213530.13	M0179
1034	2027-01-28	9463.74	2669.13	0.00	0.00	DUE	LN0021	17	204066.39	M0179
1035	2027-02-28	9582.04	2550.83	0.00	0.00	DUE	LN0021	18	194484.35	M0179
1036	2027-03-28	9701.81	2431.05	0.00	0.00	DUE	LN0021	19	184782.54	M0179
1037	2027-04-28	9823.08	2309.78	0.00	0.00	DUE	LN0021	20	174959.46	M0179
1038	2027-05-28	9945.87	2186.99	0.00	0.00	DUE	LN0021	21	165013.59	M0179
1039	2027-06-28	10070.20	2062.67	0.00	0.00	DUE	LN0021	22	154943.39	M0179
1040	2027-07-28	10196.07	1936.79	0.00	0.00	DUE	LN0021	23	144747.32	M0179
1041	2027-08-28	10323.52	1809.34	0.00	0.00	DUE	LN0021	24	134423.80	M0179
1042	2027-09-28	10452.57	1680.30	0.00	0.00	DUE	LN0021	25	123971.23	M0179
1043	2027-10-28	10583.22	1549.64	0.00	0.00	DUE	LN0021	26	113388.00	M0179
1044	2027-11-28	10715.51	1417.35	0.00	0.00	DUE	LN0021	27	102672.49	M0179
1045	2027-12-28	10849.46	1283.41	0.00	0.00	DUE	LN0021	28	91823.03	M0179
1046	2028-01-28	10985.08	1147.79	0.00	0.00	DUE	LN0021	29	80837.95	M0179
1047	2028-02-28	11122.39	1010.47	0.00	0.00	DUE	LN0021	30	69715.56	M0179
1048	2028-03-28	11261.42	871.44	0.00	0.00	DUE	LN0021	31	58454.14	M0179
1049	2028-04-28	11402.19	730.68	0.00	0.00	DUE	LN0021	32	47051.95	M0179
1050	2028-05-28	11544.72	588.15	0.00	0.00	DUE	LN0021	33	35507.24	M0179
1051	2028-06-28	11689.02	443.84	0.00	0.00	DUE	LN0021	34	23818.21	M0179
1052	2028-07-28	11835.14	297.73	0.00	0.00	DUE	LN0021	35	11983.08	M0179
1053	2028-08-28	11983.08	149.79	0.00	0.00	DUE	LN0021	36	0.00	M0179
1054	2025-09-30	17047.80	5081.31	0.00	0.00	DUE	LN0022	1	389457.20	M0180
1055	2025-10-30	17260.89	4868.22	0.00	0.00	DUE	LN0022	2	372196.31	M0180
1056	2025-11-30	17476.66	4652.45	0.00	0.00	DUE	LN0022	3	354719.65	M0180
1057	2025-12-30	17695.11	4434.00	0.00	0.00	DUE	LN0022	4	337024.54	M0180
1058	2026-01-30	17916.30	4212.81	0.00	0.00	DUE	LN0022	5	319108.23	M0180
1059	2026-02-28	18140.26	3988.85	0.00	0.00	DUE	LN0022	6	300967.98	M0180
1060	2026-03-28	18367.01	3762.10	0.00	0.00	DUE	LN0022	7	282600.97	M0180
1061	2026-04-28	18596.60	3532.51	0.00	0.00	DUE	LN0022	8	264004.37	M0180
1062	2026-05-28	18829.06	3300.05	0.00	0.00	DUE	LN0022	9	245175.31	M0180
1063	2026-06-28	19064.42	3064.69	0.00	0.00	DUE	LN0022	10	226110.89	M0180
1064	2026-07-28	19302.72	2826.39	0.00	0.00	DUE	LN0022	11	206808.17	M0180
1065	2026-08-28	19544.01	2585.10	0.00	0.00	DUE	LN0022	12	187264.16	M0180
1066	2026-09-28	19788.31	2340.80	0.00	0.00	DUE	LN0022	13	167475.85	M0180
1067	2026-10-28	20035.66	2093.45	0.00	0.00	DUE	LN0022	14	147440.19	M0180
1068	2026-11-28	20286.11	1843.00	0.00	0.00	DUE	LN0022	15	127154.09	M0180
1069	2026-12-28	20539.68	1589.43	0.00	0.00	DUE	LN0022	16	106614.40	M0180
1070	2027-01-28	20796.43	1332.68	0.00	0.00	DUE	LN0022	17	85817.97	M0180
1071	2027-02-28	21056.39	1072.72	0.00	0.00	DUE	LN0022	18	64761.59	M0180
1072	2027-03-28	21319.59	809.52	0.00	0.00	DUE	LN0022	19	43442.00	M0180
1073	2027-04-28	21586.09	543.02	0.00	0.00	DUE	LN0022	20	21855.91	M0180
1074	2027-05-28	21855.91	273.20	0.00	0.00	DUE	LN0022	21	0.00	M0180
1075	2025-09-30	14249.21	2290.62	0.00	0.00	DUE	LN0023	1	169000.79	M0182
1076	2025-10-30	14427.33	2112.51	0.00	0.00	DUE	LN0023	2	154573.46	M0182
1077	2025-11-30	14607.67	1932.17	0.00	0.00	DUE	LN0023	3	139965.80	M0182
1078	2025-12-30	14790.26	1749.57	0.00	0.00	DUE	LN0023	4	125175.53	M0182
1079	2026-01-30	14975.14	1564.69	0.00	0.00	DUE	LN0023	5	110200.39	M0182
1080	2026-02-28	15162.33	1377.50	0.00	0.00	DUE	LN0023	6	95038.06	M0182
1081	2026-03-28	15351.86	1187.98	0.00	0.00	DUE	LN0023	7	79686.20	M0182
1082	2026-04-28	15543.76	996.08	0.00	0.00	DUE	LN0023	8	64142.44	M0182
1083	2026-05-28	15738.06	801.78	0.00	0.00	DUE	LN0023	9	48404.39	M0182
1084	2026-06-28	15934.78	605.05	0.00	0.00	DUE	LN0023	10	32469.61	M0182
1085	2026-07-28	16133.97	405.87	0.00	0.00	DUE	LN0023	11	16335.64	M0182
1086	2026-08-28	16335.64	204.20	0.00	0.00	DUE	LN0023	12	0.00	M0182
1087	2025-09-30	5425.22	1192.95	0.00	0.00	DUE	LN0024	1	90010.78	M0186
1088	2025-10-30	5493.04	1125.13	0.00	0.00	DUE	LN0024	2	84517.74	M0186
1089	2025-11-30	5561.70	1056.47	0.00	0.00	DUE	LN0024	3	78956.04	M0186
1090	2025-12-30	5631.22	986.95	0.00	0.00	DUE	LN0024	4	73324.81	M0186
1091	2026-01-30	5701.61	916.56	0.00	0.00	DUE	LN0024	5	67623.20	M0186
1092	2026-02-28	5772.88	845.29	0.00	0.00	DUE	LN0024	6	61850.31	M0186
1093	2026-03-28	5845.04	773.13	0.00	0.00	DUE	LN0024	7	56005.27	M0186
1094	2026-04-28	5918.11	700.07	0.00	0.00	DUE	LN0024	8	50087.16	M0186
1095	2026-05-28	5992.08	626.09	0.00	0.00	DUE	LN0024	9	44095.08	M0186
1096	2026-06-28	6066.99	551.19	0.00	0.00	DUE	LN0024	10	38028.09	M0186
1097	2026-07-28	6142.82	475.35	0.00	0.00	DUE	LN0024	11	31885.27	M0186
1098	2026-08-28	6219.61	398.57	0.00	0.00	DUE	LN0024	12	25665.66	M0186
1099	2026-09-28	6297.35	320.82	0.00	0.00	DUE	LN0024	13	19368.31	M0186
1100	2026-10-28	6376.07	242.10	0.00	0.00	DUE	LN0024	14	12992.24	M0186
1101	2026-11-28	6455.77	162.40	0.00	0.00	DUE	LN0024	15	6536.47	M0186
1102	2026-12-28	6536.47	81.71	0.00	0.00	DUE	LN0024	16	0.00	M0186
1103	2025-09-30	7212.00	90.15	0.00	0.00	DUE	LN0025	1	0.00	M0195
1104	2025-09-30	37467.83	942.55	0.00	0.00	DUE	LN0026	1	37936.17	M0197
1105	2025-10-30	37936.17	474.20	0.00	0.00	DUE	LN0026	2	0.00	M0197
1106	2025-09-30	6649.60	3750.00	0.00	0.00	DUE	LN0027	1	293350.40	M0203
1107	2025-10-30	6732.72	3666.88	0.00	0.00	DUE	LN0027	2	286617.68	M0203
1108	2025-11-30	6816.88	3582.72	0.00	0.00	DUE	LN0027	3	279800.81	M0203
1109	2025-12-30	6902.09	3497.51	0.00	0.00	DUE	LN0027	4	272898.72	M0203
1110	2026-01-30	6988.36	3411.23	0.00	0.00	DUE	LN0027	5	265910.35	M0203
1111	2026-02-28	7075.72	3323.88	0.00	0.00	DUE	LN0027	6	258834.63	M0203
1112	2026-03-28	7164.17	3235.43	0.00	0.00	DUE	LN0027	7	251670.47	M0203
1113	2026-04-28	7253.72	3145.88	0.00	0.00	DUE	LN0027	8	244416.75	M0203
1114	2026-05-28	7344.39	3055.21	0.00	0.00	DUE	LN0027	9	237072.36	M0203
1115	2026-06-28	7436.19	2963.40	0.00	0.00	DUE	LN0027	10	229636.17	M0203
1116	2026-07-28	7529.15	2870.45	0.00	0.00	DUE	LN0027	11	222107.02	M0203
1117	2026-08-28	7623.26	2776.34	0.00	0.00	DUE	LN0027	12	214483.76	M0203
1118	2026-09-28	7718.55	2681.05	0.00	0.00	DUE	LN0027	13	206765.21	M0203
1119	2026-10-28	7815.03	2584.57	0.00	0.00	DUE	LN0027	14	198950.17	M0203
1120	2026-11-28	7912.72	2486.88	0.00	0.00	DUE	LN0027	15	191037.45	M0203
1121	2026-12-28	8011.63	2387.97	0.00	0.00	DUE	LN0027	16	183025.82	M0203
1122	2027-01-28	8111.78	2287.82	0.00	0.00	DUE	LN0027	17	174914.05	M0203
1123	2027-02-28	8213.17	2186.43	0.00	0.00	DUE	LN0027	18	166700.87	M0203
1124	2027-03-28	8315.84	2083.76	0.00	0.00	DUE	LN0027	19	158385.04	M0203
1125	2027-04-28	8419.79	1979.81	0.00	0.00	DUE	LN0027	20	149965.25	M0203
1126	2027-05-28	8525.03	1874.57	0.00	0.00	DUE	LN0027	21	141440.22	M0203
1127	2027-06-28	8631.60	1768.00	0.00	0.00	DUE	LN0027	22	132808.62	M0203
1128	2027-07-28	8739.49	1660.11	0.00	0.00	DUE	LN0027	23	124069.13	M0203
1129	2027-08-28	8848.73	1550.86	0.00	0.00	DUE	LN0027	24	115220.40	M0203
1130	2027-09-28	8959.34	1440.25	0.00	0.00	DUE	LN0027	25	106261.05	M0203
1131	2027-10-28	9071.34	1328.26	0.00	0.00	DUE	LN0027	26	97189.72	M0203
1132	2027-11-28	9184.73	1214.87	0.00	0.00	DUE	LN0027	27	88004.99	M0203
1133	2027-12-28	9299.54	1100.06	0.00	0.00	DUE	LN0027	28	78705.45	M0203
1134	2028-01-28	9415.78	983.82	0.00	0.00	DUE	LN0027	29	69289.67	M0203
1135	2028-02-28	9533.48	866.12	0.00	0.00	DUE	LN0027	30	59756.20	M0203
1136	2028-03-28	9652.65	746.95	0.00	0.00	DUE	LN0027	31	50103.55	M0203
1137	2028-04-28	9773.30	626.29	0.00	0.00	DUE	LN0027	32	40330.25	M0203
1138	2028-05-28	9895.47	504.13	0.00	0.00	DUE	LN0027	33	30434.78	M0203
1139	2028-06-28	10019.16	380.43	0.00	0.00	DUE	LN0027	34	20415.61	M0203
1140	2028-07-28	10144.40	255.20	0.00	0.00	DUE	LN0027	35	10271.21	M0203
1141	2028-08-28	10271.21	128.39	0.00	0.00	DUE	LN0027	36	0.00	M0203
1142	2025-09-30	8155.47	2832.81	0.00	0.00	DUE	LN0028	1	218469.53	M0204
1143	2025-10-30	8257.42	2730.87	0.00	0.00	DUE	LN0028	2	210212.11	M0204
1144	2025-11-30	8360.64	2627.65	0.00	0.00	DUE	LN0028	3	201851.47	M0204
1145	2025-12-30	8465.14	2523.14	0.00	0.00	DUE	LN0028	4	193386.33	M0204
1146	2026-01-30	8570.96	2417.33	0.00	0.00	DUE	LN0028	5	184815.37	M0204
1147	2026-02-28	8678.09	2310.19	0.00	0.00	DUE	LN0028	6	176137.28	M0204
1148	2026-03-28	8786.57	2201.72	0.00	0.00	DUE	LN0028	7	167350.71	M0204
1149	2026-04-28	8896.40	2091.88	0.00	0.00	DUE	LN0028	8	158454.30	M0204
1150	2026-05-28	9007.61	1980.68	0.00	0.00	DUE	LN0028	9	149446.70	M0204
1151	2026-06-28	9120.20	1868.08	0.00	0.00	DUE	LN0028	10	140326.49	M0204
1152	2026-07-28	9234.21	1754.08	0.00	0.00	DUE	LN0028	11	131092.29	M0204
1153	2026-08-28	9349.63	1638.65	0.00	0.00	DUE	LN0028	12	121742.66	M0204
1154	2026-09-28	9466.50	1521.78	0.00	0.00	DUE	LN0028	13	112276.15	M0204
1155	2026-10-28	9584.83	1403.45	0.00	0.00	DUE	LN0028	14	102691.32	M0204
1156	2026-11-28	9704.65	1283.64	0.00	0.00	DUE	LN0028	15	92986.67	M0204
1157	2026-12-28	9825.95	1162.33	0.00	0.00	DUE	LN0028	16	83160.72	M0204
1158	2027-01-28	9948.78	1039.51	0.00	0.00	DUE	LN0028	17	73211.94	M0204
1159	2027-02-28	10073.14	915.15	0.00	0.00	DUE	LN0028	18	63138.80	M0204
1160	2027-03-28	10199.05	789.24	0.00	0.00	DUE	LN0028	19	52939.75	M0204
1161	2027-04-28	10326.54	661.75	0.00	0.00	DUE	LN0028	20	42613.21	M0204
1162	2027-05-28	10455.62	532.67	0.00	0.00	DUE	LN0028	21	32157.59	M0204
1163	2027-06-28	10586.32	401.97	0.00	0.00	DUE	LN0028	22	21571.27	M0204
1164	2027-07-28	10718.65	269.64	0.00	0.00	DUE	LN0028	23	10852.63	M0204
1165	2027-08-28	10852.63	135.66	0.00	0.00	DUE	LN0028	24	0.00	M0204
1166	2025-09-30	7757.86	4375.00	0.00	0.00	DUE	LN0029	1	342242.14	M0206
1167	2025-10-30	7854.84	4278.03	0.00	0.00	DUE	LN0029	2	334387.30	M0206
1168	2025-11-30	7953.02	4179.84	0.00	0.00	DUE	LN0029	3	326434.27	M0206
1169	2025-12-30	8052.44	4080.43	0.00	0.00	DUE	LN0029	4	318381.84	M0206
1170	2026-01-30	8153.09	3979.77	0.00	0.00	DUE	LN0029	5	310228.74	M0206
1171	2026-02-28	8255.01	3877.86	0.00	0.00	DUE	LN0029	6	301973.74	M0206
1172	2026-03-28	8358.19	3774.67	0.00	0.00	DUE	LN0029	7	293615.55	M0206
1173	2026-04-28	8462.67	3670.19	0.00	0.00	DUE	LN0029	8	285152.87	M0206
1174	2026-05-28	8568.45	3564.41	0.00	0.00	DUE	LN0029	9	276584.42	M0206
1175	2026-06-28	8675.56	3457.31	0.00	0.00	DUE	LN0029	10	267908.86	M0206
1176	2026-07-28	8784.00	3348.86	0.00	0.00	DUE	LN0029	11	259124.86	M0206
1177	2026-08-28	8893.80	3239.06	0.00	0.00	DUE	LN0029	12	250231.05	M0206
1178	2026-09-28	9004.98	3127.89	0.00	0.00	DUE	LN0029	13	241226.08	M0206
1179	2026-10-28	9117.54	3015.33	0.00	0.00	DUE	LN0029	14	232108.54	M0206
1180	2026-11-28	9231.51	2901.36	0.00	0.00	DUE	LN0029	15	222877.03	M0206
1181	2026-12-28	9346.90	2785.96	0.00	0.00	DUE	LN0029	16	213530.13	M0206
1182	2027-01-28	9463.74	2669.13	0.00	0.00	DUE	LN0029	17	204066.39	M0206
1183	2027-02-28	9582.04	2550.83	0.00	0.00	DUE	LN0029	18	194484.35	M0206
1184	2027-03-28	9701.81	2431.05	0.00	0.00	DUE	LN0029	19	184782.54	M0206
1185	2027-04-28	9823.08	2309.78	0.00	0.00	DUE	LN0029	20	174959.46	M0206
1186	2027-05-28	9945.87	2186.99	0.00	0.00	DUE	LN0029	21	165013.59	M0206
1187	2027-06-28	10070.20	2062.67	0.00	0.00	DUE	LN0029	22	154943.39	M0206
1188	2027-07-28	10196.07	1936.79	0.00	0.00	DUE	LN0029	23	144747.32	M0206
1189	2027-08-28	10323.52	1809.34	0.00	0.00	DUE	LN0029	24	134423.80	M0206
1190	2027-09-28	10452.57	1680.30	0.00	0.00	DUE	LN0029	25	123971.23	M0206
1191	2027-10-28	10583.22	1549.64	0.00	0.00	DUE	LN0029	26	113388.00	M0206
1192	2027-11-28	10715.51	1417.35	0.00	0.00	DUE	LN0029	27	102672.49	M0206
1193	2027-12-28	10849.46	1283.41	0.00	0.00	DUE	LN0029	28	91823.03	M0206
1194	2028-01-28	10985.08	1147.79	0.00	0.00	DUE	LN0029	29	80837.95	M0206
1195	2028-02-28	11122.39	1010.47	0.00	0.00	DUE	LN0029	30	69715.56	M0206
1196	2028-03-28	11261.42	871.44	0.00	0.00	DUE	LN0029	31	58454.14	M0206
1197	2028-04-28	11402.19	730.68	0.00	0.00	DUE	LN0029	32	47051.95	M0206
1198	2028-05-28	11544.72	588.15	0.00	0.00	DUE	LN0029	33	35507.24	M0206
1199	2028-06-28	11689.02	443.84	0.00	0.00	DUE	LN0029	34	23818.21	M0206
1200	2028-07-28	11835.14	297.73	0.00	0.00	DUE	LN0029	35	11983.08	M0206
1201	2028-08-28	11983.08	149.79	0.00	0.00	DUE	LN0029	36	0.00	M0206
1202	2025-09-30	7591.34	2020.89	0.00	0.00	DUE	LN0030	1	154079.66	M0208
1203	2025-10-30	7686.23	1926.00	0.00	0.00	DUE	LN0030	2	146393.43	M0208
1204	2025-11-30	7782.31	1829.92	0.00	0.00	DUE	LN0030	3	138611.12	M0208
1205	2025-12-30	7879.59	1732.64	0.00	0.00	DUE	LN0030	4	130731.53	M0208
1206	2026-01-30	7978.08	1634.14	0.00	0.00	DUE	LN0030	5	122753.45	M0208
1207	2026-02-28	8077.81	1534.42	0.00	0.00	DUE	LN0030	6	114675.64	M0208
1208	2026-03-28	8178.78	1433.45	0.00	0.00	DUE	LN0030	7	106496.86	M0208
1209	2026-04-28	8281.02	1331.21	0.00	0.00	DUE	LN0030	8	98215.84	M0208
1210	2026-05-28	8384.53	1227.70	0.00	0.00	DUE	LN0030	9	89831.32	M0208
1211	2026-06-28	8489.34	1122.89	0.00	0.00	DUE	LN0030	10	81341.98	M0208
1212	2026-07-28	8595.45	1016.77	0.00	0.00	DUE	LN0030	11	72746.53	M0208
1213	2026-08-28	8702.90	909.33	0.00	0.00	DUE	LN0030	12	64043.63	M0208
1214	2026-09-28	8811.68	800.55	0.00	0.00	DUE	LN0030	13	55231.95	M0208
1215	2026-10-28	8921.83	690.40	0.00	0.00	DUE	LN0030	14	46310.12	M0208
1216	2026-11-28	9033.35	578.88	0.00	0.00	DUE	LN0030	15	37276.77	M0208
1217	2026-12-28	9146.27	465.96	0.00	0.00	DUE	LN0030	16	28130.51	M0208
1218	2027-01-28	9260.60	351.63	0.00	0.00	DUE	LN0030	17	18869.91	M0208
1219	2027-02-28	9376.35	235.87	0.00	0.00	DUE	LN0030	18	9493.56	M0208
1220	2027-03-28	9493.56	118.67	0.00	0.00	DUE	LN0030	19	0.00	M0208
1221	2025-09-30	4318.40	1500.00	0.00	0.00	DUE	LN0031	1	115681.60	M0224
1222	2025-10-30	4372.38	1446.02	0.00	0.00	DUE	LN0031	2	111309.22	M0224
1223	2025-11-30	4427.03	1391.37	0.00	0.00	DUE	LN0031	3	106882.19	M0224
1224	2025-12-30	4482.37	1336.03	0.00	0.00	DUE	LN0031	4	102399.82	M0224
1225	2026-01-30	4538.40	1280.00	0.00	0.00	DUE	LN0031	5	97861.42	M0224
1226	2026-02-28	4595.13	1223.27	0.00	0.00	DUE	LN0031	6	93266.29	M0224
1227	2026-03-28	4652.57	1165.83	0.00	0.00	DUE	LN0031	7	88613.72	M0224
1228	2026-04-28	4710.73	1107.67	0.00	0.00	DUE	LN0031	8	83903.00	M0224
1229	2026-05-28	4769.61	1048.79	0.00	0.00	DUE	LN0031	9	79133.39	M0224
1230	2026-06-28	4829.23	989.17	0.00	0.00	DUE	LN0031	10	74304.16	M0224
1231	2026-07-28	4889.60	928.80	0.00	0.00	DUE	LN0031	11	69414.56	M0224
1232	2026-08-28	4950.72	867.68	0.00	0.00	DUE	LN0031	12	64463.84	M0224
1233	2026-09-28	5012.60	805.80	0.00	0.00	DUE	LN0031	13	59451.24	M0224
1234	2026-10-28	5075.26	743.14	0.00	0.00	DUE	LN0031	14	54375.99	M0224
1235	2026-11-28	5138.70	679.70	0.00	0.00	DUE	LN0031	15	49237.29	M0224
1236	2026-12-28	5202.93	615.47	0.00	0.00	DUE	LN0031	16	44034.36	M0224
1237	2027-01-28	5267.97	550.43	0.00	0.00	DUE	LN0031	17	38766.39	M0224
1238	2027-02-28	5333.82	484.58	0.00	0.00	DUE	LN0031	18	33432.57	M0224
1239	2027-03-28	5400.49	417.91	0.00	0.00	DUE	LN0031	19	28032.08	M0224
1240	2027-04-28	5468.00	350.40	0.00	0.00	DUE	LN0031	20	22564.08	M0224
1241	2027-05-28	5536.35	282.05	0.00	0.00	DUE	LN0031	21	17027.74	M0224
1242	2027-06-28	5605.55	212.85	0.00	0.00	DUE	LN0031	22	11422.19	M0224
1243	2027-07-28	5675.62	142.78	0.00	0.00	DUE	LN0031	23	5746.57	M0224
1244	2027-08-28	5746.57	71.83	0.00	0.00	DUE	LN0031	24	0.00	M0224
1245	2025-09-30	6374.79	2540.42	0.00	0.00	DUE	LN0032	1	196859.21	M0244
1246	2025-10-30	6454.48	2460.74	0.00	0.00	DUE	LN0032	2	190404.73	M0244
1247	2025-11-30	6535.16	2380.06	0.00	0.00	DUE	LN0032	3	183869.57	M0244
1248	2025-12-30	6616.85	2298.37	0.00	0.00	DUE	LN0032	4	177252.72	M0244
1249	2026-01-30	6699.56	2215.66	0.00	0.00	DUE	LN0032	5	170553.16	M0244
1250	2026-02-28	6783.30	2131.91	0.00	0.00	DUE	LN0032	6	163769.85	M0244
1251	2026-03-28	6868.10	2047.12	0.00	0.00	DUE	LN0032	7	156901.76	M0244
1252	2026-04-28	6953.95	1961.27	0.00	0.00	DUE	LN0032	8	149947.81	M0244
1253	2026-05-28	7040.87	1874.35	0.00	0.00	DUE	LN0032	9	142906.94	M0244
1254	2026-06-28	7128.88	1786.34	0.00	0.00	DUE	LN0032	10	135778.06	M0244
1255	2026-07-28	7217.99	1697.23	0.00	0.00	DUE	LN0032	11	128560.06	M0244
1256	2026-08-28	7308.22	1607.00	0.00	0.00	DUE	LN0032	12	121251.85	M0244
1257	2026-09-28	7399.57	1515.65	0.00	0.00	DUE	LN0032	13	113852.27	M0244
1258	2026-10-28	7492.07	1423.15	0.00	0.00	DUE	LN0032	14	106360.21	M0244
1259	2026-11-28	7585.72	1329.50	0.00	0.00	DUE	LN0032	15	98774.49	M0244
1260	2026-12-28	7680.54	1234.68	0.00	0.00	DUE	LN0032	16	91093.95	M0244
1261	2027-01-28	7776.54	1138.67	0.00	0.00	DUE	LN0032	17	83317.41	M0244
1262	2027-02-28	7873.75	1041.47	0.00	0.00	DUE	LN0032	18	75443.66	M0244
1263	2027-03-28	7972.17	943.05	0.00	0.00	DUE	LN0032	19	67471.49	M0244
1264	2027-04-28	8071.83	843.39	0.00	0.00	DUE	LN0032	20	59399.66	M0244
1265	2027-05-28	8172.72	742.50	0.00	0.00	DUE	LN0032	21	51226.94	M0244
1266	2027-06-28	8274.88	640.34	0.00	0.00	DUE	LN0032	22	42952.05	M0244
1267	2027-07-28	8378.32	536.90	0.00	0.00	DUE	LN0032	23	34573.74	M0244
1268	2027-08-28	8483.05	432.17	0.00	0.00	DUE	LN0032	24	26090.69	M0244
1269	2027-09-28	8589.09	326.13	0.00	0.00	DUE	LN0032	25	17501.60	M0244
1270	2027-10-28	8696.45	218.77	0.00	0.00	DUE	LN0032	26	8805.15	M0244
1271	2027-11-28	8805.15	110.06	0.00	0.00	DUE	LN0032	27	0.00	M0244
1272	2025-09-30	17861.10	4475.59	0.00	0.00	DUE	LN0033	1	340185.90	M0246
1273	2025-10-30	18084.36	4252.32	0.00	0.00	DUE	LN0033	2	322101.54	M0246
1274	2025-11-30	18310.42	4026.27	0.00	0.00	DUE	LN0033	3	303791.12	M0246
1275	2025-12-30	18539.30	3797.39	0.00	0.00	DUE	LN0033	4	285251.83	M0246
1276	2026-01-30	18771.04	3565.65	0.00	0.00	DUE	LN0033	5	266480.79	M0246
1277	2026-02-28	19005.68	3331.01	0.00	0.00	DUE	LN0033	6	247475.11	M0246
1278	2026-03-28	19243.25	3093.44	0.00	0.00	DUE	LN0033	7	228231.86	M0246
1279	2026-04-28	19483.79	2852.90	0.00	0.00	DUE	LN0033	8	208748.08	M0246
1280	2026-05-28	19727.33	2609.35	0.00	0.00	DUE	LN0033	9	189020.74	M0246
1281	2026-06-28	19973.93	2362.76	0.00	0.00	DUE	LN0033	10	169046.82	M0246
1282	2026-07-28	20223.60	2113.09	0.00	0.00	DUE	LN0033	11	148823.21	M0246
1283	2026-08-28	20476.40	1860.29	0.00	0.00	DUE	LN0033	12	128346.82	M0246
1284	2026-09-28	20732.35	1604.34	0.00	0.00	DUE	LN0033	13	107614.47	M0246
1285	2026-10-28	20991.51	1345.18	0.00	0.00	DUE	LN0033	14	86622.96	M0246
1286	2026-11-28	21253.90	1082.79	0.00	0.00	DUE	LN0033	15	65369.06	M0246
1287	2026-12-28	21519.57	817.11	0.00	0.00	DUE	LN0033	16	43849.49	M0246
1288	2027-01-28	21788.57	548.12	0.00	0.00	DUE	LN0033	17	22060.92	M0246
1289	2027-02-28	22060.92	275.76	0.00	0.00	DUE	LN0033	18	0.00	M0246
\.


--
-- Data for Name: loans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loans (id, status, loan_no, member_no, loan_account, interest_account, interest_rate, disbursed_date, created_at, loan_amount, loan_period, balance, disbursed_by, interest_balance, loan_type) FROM stdin;
30	Active	LN0002	M0009	M0009_LOAN	M0009_INTEREST	15.00	2025-07-06	2025-10-25 12:12:14.467877	150000.00	12	134500.00	1	0.00	NORMAL
31	Active	LN0003	M0010	M0010_LOAN	M0010_INTEREST	15.00	2024-08-04	2025-10-25 12:12:14.467877	180000.00	36	170135.00	1	0.00	NORMAL
32	Active	LN0004	M0011	M0011_LOAN	M0011_INTEREST	15.00	2024-08-15	2025-10-25 12:12:14.467877	460000.00	36	179668.00	1	0.00	NORMAL
33	Active	LN0005	M0022	M0022_LOAN	M0022_INTEREST	15.00	2024-05-13	2025-10-25 12:12:14.467877	280000.00	24	108168.00	1	0.00	NORMAL
34	Active	LN0006	M0023	M0023_LOAN	M0023_INTEREST	15.00	2025-08-04	2025-10-25 12:12:14.467877	180000.00	36	180000.00	1	0.00	NORMAL
35	Active	LN0007	M0027	M0027_LOAN	M0027_INTEREST	15.00	2025-04-18	2025-10-25 12:12:14.467877	420000.00	36	382082.00	1	0.00	NORMAL
36	Active	LN0008	M0051	M0051_LOAN	M0051_INTEREST	15.00	2024-10-01	2025-10-25 12:12:14.467877	840000.00	36	761724.00	1	0.00	NORMAL
37	Active	LN0009	M0054	M0054_LOAN	M0054_INTEREST	15.00	2024-04-22	2025-10-25 12:12:14.467877	30000.00	12	21362.00	1	0.00	NORMAL
38	Active	LN0010	M0059	M0059_LOAN	M0059_INTEREST	15.00	2025-03-05	2025-10-25 12:12:14.467877	620000.00	36	620000.00	1	0.00	NORMAL
39	Active	LN0011	M0063	M0063_LOAN	M0063_INTEREST	15.00	2024-06-08	2025-10-25 12:12:14.467877	300000.00	24	125245.00	1	0.00	NORMAL
40	Active	LN0012	M0076	M0076_LOAN	M0076_INTEREST	15.00	2025-07-14	2025-10-25 12:12:14.467877	1000000.00	36	795871.00	1	0.00	NORMAL
41	Active	LN0013	M0079	M0079_LOAN	M0079_INTEREST	15.00	2024-07-03	2025-10-25 12:12:14.467877	60000.00	24	58540.00	1	0.00	NORMAL
42	Active	LN0014	M0123	M0123_LOAN	M0123_INTEREST	15.00	2024-05-13	2025-10-25 12:12:14.467877	200000.00	24	158664.00	1	0.00	NORMAL
43	Active	LN0015	M0131	M0131_LOAN	M0131_INTEREST	15.00	2024-04-03	2025-10-25 12:12:14.467877	30000.00	12	17964.00	1	0.00	NORMAL
44	Active	LN0016	M0163	M0163_LOAN	M0163_INTEREST	15.00	2023-04-14	2025-10-25 12:12:14.467877	20000.00	12	10118.00	1	0.00	NORMAL
45	Active	LN0017	M0166	M0166_LOAN	M0166_INTEREST	15.00	2024-11-04	2025-10-25 12:12:14.467877	750000.00	36	677801.00	1	0.00	NORMAL
46	Active	LN0018	M0168	M0168_LOAN	M0168_INTEREST	15.00	2023-04-28	2025-10-25 12:12:14.467877	300000.00	24	228356.00	1	0.00	NORMAL
47	Active	LN0019	M0171	M0171_LOAN	M0171_INTEREST	15.00	2025-04-12	2025-10-25 12:12:14.467877	620000.00	24	581341.00	1	0.00	NORMAL
48	Active	LN0020	M0174	M0174_LOAN	M0174_INTEREST	15.00	2024-08-31	2025-10-25 12:12:14.467877	100000.00	12	13917.00	1	0.00	NORMAL
49	Active	LN0021	M0179	M0179_LOAN	M0179_INTEREST	15.00	2025-08-04	2025-10-25 12:12:14.467877	350000.00	36	350000.00	1	0.00	NORMAL
50	Active	LN0022	M0180	M0180_LOAN	M0180_INTEREST	15.00	2025-05-30	2025-10-25 12:23:48.123091	500000.00	24	406505.00	1	0.00	NORMAL
51	Active	LN0023	M0182	M0182_LOAN	M0182_INTEREST	15.00	2024-08-05	2025-10-25 12:23:48.123091	270000.00	24	183250.00	1	0.00	NORMAL
52	Active	LN0024	M0186	M0186_LOAN	M0186_INTEREST	15.00	2024-12-11	2025-10-25 12:23:48.123091	150000.00	24	95436.00	1	0.00	NORMAL
53	Active	LN0025	M0195	M0195_LOAN	M0195_INTEREST	15.00	2024-05-02	2025-10-25 12:23:48.123091	15000.00	12	7212.00	1	0.00	NORMAL
54	Active	LN0026	M0197	M0197_LOAN	M0197_INTEREST	15.00	2025-04-25	2025-10-25 12:23:48.123091	100000.00	6	75404.00	1	0.00	NORMAL
55	Active	LN0027	M0203	M0203_LOAN	M0203_INTEREST	15.00	2025-08-12	2025-10-25 12:23:48.123091	300000.00	36	300000.00	1	0.00	NORMAL
56	Active	LN0028	M0204	M0204_LOAN	M0204_INTEREST	15.00	2024-08-22	2025-10-25 12:23:48.123091	300000.00	36	226625.00	1	0.00	NORMAL
57	Active	LN0029	M0206	M0206_LOAN	M0206_INTEREST	15.00	2025-08-04	2025-10-25 12:23:48.123091	350000.00	36	350000.00	1	0.00	NORMAL
58	Active	LN0030	M0208	M0208_LOAN	M0208_INTEREST	15.00	2024-03-04	2025-10-25 12:23:48.123091	265000.00	36	161671.00	1	0.00	NORMAL
59	Active	LN0031	M0224	M0224_LOAN	M0224_INTEREST	15.00	2025-08-09	2025-10-25 12:23:48.123091	120000.00	24	120000.00	1	0.00	NORMAL
60	Active	LN0032	M0244	M0244_LOAN	M0244_INTEREST	15.00	2024-11-20	2025-10-25 12:23:48.123091	300000.00	36	203234.00	1	0.00	NORMAL
61	Active	LN0033	M0246	M0246_LOAN	M0246_INTEREST	15.00	2025-02-05	2025-10-25 12:23:48.123091	500000.00	24	358047.00	1	0.00	NORMAL
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.members (id, member_no, name, phone, email, joined_date, dob, id_no, congregation, gender, created_by) FROM stdin;
289	M000GL	PCEA CHAIRETE SACCO	254721313527	kariokojim@gmail.com	2025-10-18	\N	\N	MACEDONIA	\N	1
290	M0001	Rev David Muthui	254720233004	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
291	M0002	Esther Githuka	254722713915	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
292	M0003	Gideon Karanja	254721910061	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
293	M0004	Cleophas Barmasai	254729955964	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
294	M0005	Joseph Maina	254722613464	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
295	M0006	Gerald Gitonga	254722286884	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
296	M0007	Jean Wahome	254722700222	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
297	M0008	Henry Ndungu	254721456386	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
298	M0009	Jane Ndirangu	254722883628	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
299	M0010	Joseph Wambugu	254710459815	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
300	M0011	Paul Nyatha	254727373063	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
301	M0012	Peter Gitau	254722311270	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
302	M0013	Brigdit Melau	254722847535	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
303	M0014	Peter Nyoike	254722609846	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
304	M0015	Nancy Wanjiru Mwangi	254722450712	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
305	M0016	Stephen M Njenga	254722366172	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
306	M0017	Mary Nakeel	254720705969	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
307	M0018	Jane Kaimuri	254723156905	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
308	M0019	Kennedy Kinyua	254702526290	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
309	M0020	Peter Melonye	254722614583	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
310	M0021	James Muiruri	254721313527	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
311	M0022	Simon Gathura	254722326626	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
312	M0023	John Mbugua	254722873389	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
313	M0024	Gladys Wambui Musijo	254726361261	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
314	M0025	Muruu Wa Muthonga	254723803502	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
315	M0026	Livingstone Ndereba	254726802631	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
316	M0027	Dorcas Mbura Muturi	254722560500	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
317	M0028	Josephine Njoki Njuguna	254722390983	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
318	M0029	Mary Wawira Kiura	254714295281	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
319	M0030	Ivy Njeri Wahome	254713277361	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
320	M0031	Mary Wangari Waweru	254799090660	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
321	M0032	Samson Mbuthia Gathungu	254721550268	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
322	M0033	Mercy Wairimu	254725513578	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
323	M0034	Naomi Wangari Gitonga	254721596964	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
324	M0035	Florence Wambui	254722370351	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
325	M0036	Rosalia Mutheu	254721217519	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
326	M0037	Joseph Anthony Njuguna	254722588899	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
327	M0038	Margaret Wairimu K.	254722590556	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
328	M0039	Salome Wangari T.	254710433050	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
329	M0040	Joseph Mwangi	254700313342	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
330	M0041	Lucy Wanjiru	254723748253	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
331	M0042	Joseph Njuguna	254713773296	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
332	M0043	Geoffrey Murithi	254722266085	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
333	M0044	Walter Okwayo	254713360884	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
334	M0045	Susan Wanjiku	254728657150	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
335	M0046	Samuel Warutere	254724262687	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
336	M0047	Antony Njuguna	254720583652	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
337	M0048	Loveness Maggi H.	254722599961	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
338	M0049	Josephene Wangari	254722935163	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
339	M0050	Virginia Wambui	254724410077	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
340	M0051	P.C.E.A Ongata Chapel	254717720893	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
341	M0052	Irene Wanjiku	254723686946	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
342	M0053	Naom Wanja Ndungu	254723270112	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
343	M0054	Edith Thunguri	254722797136	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
344	M0055	Robert Gathuku M.	254722263873	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
345	M0056	Joan Wanjiru	254719772835	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
346	M0057	Samuel Ndirangu	254708906680	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
347	M0058	Shiphrah Wanjiku	254722429870	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
348	M0059	Michael Mbiriri	254721806067	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
349	M0060	James Karanja	254722453543	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
350	M0061	James Gitahi	254721605992	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
351	M0062	Richard Mathu	254722520420	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
352	M0063	Samuel Mugo W.	254722824435	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
353	M0064	Yuda Ismael Ngiluke	254741090426	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
354	M0065	Mercy Makena	254727452456	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
355	M0066	Damaris Wangeci	254721512682	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
356	M0067	Pauline Wanjiru	254724659791	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
357	M0068	Peter Runo	254728394438	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
358	M0069	Patricia Wairimu	254721490539	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
359	M0070	Annie Njeri	254721490539	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
360	M0071	Eunice Ngoiyana	254722637177	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
361	M0072	Lilian Mugure	254720214079	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
362	M0073	Jane Nyaiteyo	254792063793	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
363	M0074	Ndungu Tracy	254702898560	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
364	M0075	Jane Wambui	254716504121	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
365	M0076	Beatrice Wangechi	254710663436	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
366	M0077	Joyce Njoki Kamau	254722344806	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
367	M0078	Anne Nduta Matindi	254721681923	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
368	M0079	Pauline Metian	254725385905	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
369	M0080	Eric Maina Gitonga	254723891251	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
370	M0081	Grace Njeri	254715652518	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
371	M0082	Sammy Mwangi	254726560512	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
372	M0083	Gerald Karicho	254728796811	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
373	M0084	Daniel Mbiu	254722450230	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
374	M0085	Virginia Njoki	254721879593	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
375	M0086	Nancy Kagendo	254726706513	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
376	M0087	Margaret N. Mwangi	254720479023	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
377	M0088	Oreste Gitonga	254727797083	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
378	M0089	Susan Njoki Kanyua	254701869509	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
379	M0090	Purity Kageni Njangi	254725349525	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
380	M0091	Jane Wambui Mwangi	254725755087	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
381	M0092	James Pareiyo M.	254728587126	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
382	M0093	Jasan Kanyungo	254722457915	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
383	M0094	Susan Annie Naigu	254722550168	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
384	M0095	Nancy Njoki	254722669771	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
385	M0096	Bornface Odour	254721166542	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
386	M0097	Martin Kiarie	254722215934	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
387	M0098	Daniel Kariuki	254722803200	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
388	M0099	Godfrey Mwema	254722330639	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
389	M0100	Purity Wanjiru Njanja	254722356325	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
390	M0101	Alvine Mathu K.	254722247292	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
391	M0102	Kenson Mutembei	254722639447	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
392	M0103	George Mwangi	254728155023	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
393	M0104	Edward Mukora W.	254718556667	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
394	M0105	Peter Kariuki Muchai	254721779931	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
395	M0106	Mary Nyawira	254727127773	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
396	M0107	Grace Wambui Wandaku	254721873132	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
397	M0108	Paul Njuguna Mburu	254722392735	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
398	M0109	Nancy Nyawira Nkonge	254720718107	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
399	M0110	Xavier Mutugi	254722560925	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
400	M0111	Yvonne Njeri Gathogo	254799248500	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
401	M0112	Joyce Njeri Wango 	254704860649	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
402	M0113	Delphine Waruinu Gitonga	254720057512	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
403	M0114	Aphufia Wairimu Mwema	254729558885	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
404	M0115	Godfrey Wachira Muraga	254717163532	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
405	M0116	Wilfred Wangendo Mbugua	254714060143	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
406	M0117	Samuel Nganga Njoroge	254721438288	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
407	M0118	George Gathura Njoroge	254726073190	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
408	M0119	Annie Wambui Wainaina	254722868619	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
409	M0120	Ekra Wanja	254729036151	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
410	M0121	Livingstone M. Ochoki	254700596823	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
411	M0122	Sarah Wambui Gitau 	254724903118	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
412	M0123	Joseph Kamau Ndungu	254712666235	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
413	M0124	Samson Moijoi Morinke	254721266670	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
414	M0125	Rahab Wanjiku Gitau	254728350196	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
415	M0126	Robert Muhia Kinyanjui	254724891612	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
416	M0127	Ellam Minju Gikonyo	254703808029	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
417	M0128	John Ndungu Mwaura 	254700612090	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
418	M0129	Kenneth Kinungi Kungu	254723009196	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
419	M0130	Stephen Wambugu Thairu	254724982825	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
420	M0131	Hanna Muthoni Kanyua 	254712583339	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
421	M0132	Joseph Noel Lempuris &Deborah	254720261967	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
422	M0133	Peter Gachanja Ngabiah	254721626268	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
423	M0134	Martha Wanjiru Irungu	254721294091	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
424	M0135	Newton Maina Irungu	254705569854	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
425	M0136	Peter Kamau Muiruri	254758044838	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
426	M0137	Jeremia Mwangi Gitau	254707670743	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
427	M0138	Nancy Njoki	254726096519	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
428	M0139	Harrison Wachira Maina	254721620337	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
429	M0140	Grace Wambui Thuo	254792764473	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
430	M0141	Grace Wambui Ndungu	254721728516	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
431	M0142	Nancy Njoki Maina	254725230428	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
432	M0143	Grace Wanjiku Kamau	254758054233	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
433	M0144	Boaz Wanyeki Githogunyi	254720705551	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
434	M0145	Janerose Wanjiku Njuguna	254722321634	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
435	M0146	Laban Lemaiyan Moijoi	254703221405	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
436	M0147	P.C.E.A Baraka Parish	254729832187	test1@pceachairetesacco.com	2025-10-18	\N	\N	PARISH	\N	1
437	M0148	Kelvin Robert Mugambi Kibe	254702590307	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
438	M0149	Ruth Claire Njeri Mugambi	254721429980	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
439	M0150	Benson Ruoro Miano	254726286298	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
440	M0151	Ryan Salaon Melonye	254745284797	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
441	M0152	John Koiyaki Musijo	254726399291	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
442	M0153	Lucy Wangari Mwangi	254708000290	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
443	M0154	David Kihato Murithi	254722791610	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
444	M0155	Catherine Nyawira Ndungu	254721112094	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
445	M0156	Lillian Atieno Oloo	254713374936	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
446	M0157	Silvester Kamau Nyongesa	254712501702	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
447	M0158	Esther Mbithe Kivuva	254759276123	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
448	M0159	Elizabeth Muthoni Njuri	254721944378	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
449	M0160	Joel Gitonga KAnyua	254726578431	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
450	M0161	Eddy Stanley Kimani Gitau	254721741343	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
451	M0162	Mariah Nyaruiru Ngunjiri	254712703631	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
452	M0163	Samuel Muturi Maina	254719601011	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
453	M0164	Caroline Wangari Njuri	254724329496	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
454	M0165	Simon Ngugi Musijo	254254798799729	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
455	M0166	PAUL NDIRANGU MATHENGE	254722752931	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPELel	\N	1
456	M0167	MARY NJERI GATUNE	254721315429	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
457	M0168	JOHN KOIYAKI KARANJA	254719736705	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
458	M0169	CAROLINE WAIRIMU NJOROGE	254720346106	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
459	M0170	PAUL/FRANCIS/SAMUEL	254721228339	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPELel	\N	1
460	M0171	WILLY MUTITU NDUNGU	254724549359	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPELEL	\N	1
461	M0172	PETER&CAROL NJANJO	254712438248	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPELEL	\N	1
462	M0173	JOSEPH NGUGI KIARIE	254722504064	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
463	M0174	BERNARD MWANGI	254724455979	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
464	M0175	FRANCIS MUNYI MUKIRIA	254722717176	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
465	M0176	PCEA MACEDONIA CHURCH	254722330639	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
466	M0177	JOHN NGANGA MUNGAI	254723699735	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
467	M0178	PRISCILLA WARIGIA GATHIAKA	254722518526	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
468	M0179	JENNIFER NYAWIRA WAGURA	254724617884	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
469	M0180	JANE GATHONI NJOROGE	254722326626	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
470	M0181	ALVIN JAY GITONGA MAINA	254712761837	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
471	M0182	ALICE MUTHONI KINYAGO	254740743177	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
472	M0183	JEREMIAH NJUGUNA KARIUKI	254721928657	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
473	M0184	SAMUEL NGANGA NGUGI	254798336517	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
474	M0185	EDWIN NJOROGE GATHUTO	254795442863	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
475	M0186	SAMUEL GITONGA KIMANI	254791503404	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
476	M0187	MARYANNE WANJIRU	254757273724	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
477	M0188	TABITHA THUKU	254722785578	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
478	M0189	JULIANA NJOROGE	254721673101	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
479	M0190	ESTHER KARARI	254721406846	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
480	M0191	ALEX MAINA	254701059485	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
481	M0192	DANIEL MWANGI	254723594361	test1@pceachairetesacco.com	2025-10-18	\N	\N	NKAIMURUNYA	\N	1
482	M0193	LYDIA WANGUI	254727444490	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
483	M0194	MICHAEL KARIUKI	254721794982	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
484	M0195	LUCY WANJIKU	254713813395	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
485	M0196	MONICAH GATHUNGU	254724112372	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
486	M0197	DAVID GICHIMU	254721444306	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
487	M0198	DAVID KARANJA	254743272797	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
488	M0199	HARRISON NJOROGE	254710863891	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
489	M0200	BEATRICE IRUNGU	254723696967	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
490	M0201	BOOTH GIRLS	254013114284	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
491	M0202	RAHAB WANJIRU	254725888119	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
492	M0203	ALICE WANGUI	254724379551	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
493	M0204	CYRUS MUYA	254746173069	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
494	M0205	NANCY WACERA	254722224419	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
495	M0206	EUNICE KARANJA	254721343967	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
496	M0207	CHARITY NDIRANGU	254727798005	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
497	M0208	JOHN KAMAU	254700399407	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
498	M0209	NANCY GIKONYO	254726733151	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
499	M0210	JOHN MAINA	254723663731	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
500	M0211	IRENE MBURU	254795339631	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
501	M0212	JANE MURIITHI	254712145921	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
502	M0213	BRIAN NJUGUNA	254746652612	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
503	M0214	BELVER KATOYO	254723066409	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
504	M0215	MARY MUTAHI	254726856061	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
505	M0216	GRACE KURIA	254791299597	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
506	M0217	JOHN MUNGAI	254721901155	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
507	M0218	JOSEPH KIAMA	254706968934	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
508	M0219	BONIFACE KAMAU	254726145416	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
509	M0220	CATHERINE KABURA	254720234164	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
510	M0221	CAROL MWAURA	254722460618	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
511	M0222	ESTHER KANGANGI	254721175222	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
512	M0223	ELIZABETH GITHUI	254721512024	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
513	M0224	SULEIMAN NJUGNA	254716948127	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
514	M0225	MAUREEN WANYEKI	254768424655	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
515	M0226	NANCY WACHIRA	254722631048	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
516	M0227	JOYCE NJERI	254723954228	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
517	M0228	BEATRICE MWANGI	254720272644	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
518	M0229	VIRGINIA NJOROGE	254728285042	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
519	M0230	BEATRICE WAMBUGU	254722934982	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
520	M0231	PCEA ONGATA CHAPEL	254732910310	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
521	M0232	SCOLA MURUU	254723686649	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
522	M0233	RACHEL MBUGUA	254718207020	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
523	M0234	JOHN KAMAU	254713372857	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
524	M0235	ZIPPORAH/DORCAS/SOPHIAH	254722446067	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
525	M0236	ZIPPORAH GACIBI	254702760305	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
526	M0237	DORCAS MWANGI	254722446067	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
527	M0238	SOPHIAH MUTITU	254720087181	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
528	M0239	DAMARIS KANYUA	254714556423	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
529	M0240	ANNIE KINYANJUI	254721585405	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
530	M0241	MARY NYAMBURA	254743286628	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
531	M0242	ROSE MUTITU	254723811630	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
532	M0243	NAHASHON NDUNGU	254727462015	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
533	M0244	WONDERWELL ACADEMY	254706820380	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
534	M0245	IRENE KIBUI	254723622593	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
535	M0246	ROSE KANJU	254717404515	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
536	M0247	JOHN KIBIRU	2547230125578	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
537	M0248	ESTHER MUTHONI WANJIRU	254716865115	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
538	M0249	PAULINE WANGARI	254718207722	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
539	M0250	JOY MUKAMI GITHINJI	254713084810	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
540	M0251	ERASTUS MUGO MUNENE	254748878398	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
541	M0252	LUCY MUTHONI KIMANI	254721263215	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
542	M0253	MARTHA WANJIKU KIMANI	254725751126	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
543	M0254	MAGDALINE WANGUI KAMAU	254722592428	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
544	M0255	JUDY NYAWIRA	254727573506	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
545	M0256	JOSPHANT KABUTE IRUNGU	254711111111	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
546	M0257	JOSEPH MUNGAI	254721698913	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
547	M0258	ANTHONY KINYUA GITATA	254791480304	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
548	M0259	JAMES WAHOME GITATA	254794197901	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
549	M0260	FELIX LETOMIA KAIPEI	254790976172	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
550	M0261	SUSAN WANGU MWITITHIO	254790988972	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
551	M0262	VALARY WANJIKU MAINA 	254705949488	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
552	M0263	PCEA UPENDO CHURCH	254722450712	test1@pceachairetesacco.com	2025-10-18	\N	\N	UPENDO	\N	1
553	M0264	CAROLINE GACERI	254720417882	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
554	M0265	QUINCY NJUGUNA KARIUKI	254721940088	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
555	M0266	ESPHAN NGANGA	254703448897	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
556	M0267	RUFUS KIRIGWI MBATIA	254	test1@pceachairetesacco.com	2025-10-18	\N	\N	254722990748	\N	1
557	M0268	FIDELE SERUGO RWAGASORE	254740486688	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
558	M0280	MARGARET WANJIKU NGATHA	254725622214	test1@pceachairetesacco.com	2025-10-18	\N	\N	ONGATA CHAPEL	\N	1
559	M0281	JOSHUA K MABURI	254700921341	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
560	M0282	MARION GAKII	254720398080	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
561	M0283	LYDIA NJOKI	254702515333	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
562	M0284	CATHERINE MURIGU	254721140579	test1@pceachairetesacco.com	2025-10-18	\N	\N	MACEDONIA	\N	1
563	M0285	ANNAH WANGECI NAJU	254	test1@pceachairetesacco.com	2025-10-18	\N	\N	254721354846	\N	1
564	M0286	CHRISTINE KEMUNTO OBWAGE	254	test1@pceachairetesacco.com	2025-10-18	\N	\N	254704766863	\N	1
\.


--
-- Data for Name: sacco_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sacco_accounts (account_id, member_no, account_number, account_type, balance, "limit", status, created_at, updated_at, created_by) FROM stdin;
362	M0027	M0027_SAVINGS	SAVINGS	173380.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:08.239131	admin
452	M0117	M0117_SAVINGS	SAVINGS	129000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:27.330345	admin
532	M0197	M0197_SAVINGS	SAVINGS	45200.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:46.85317	admin
365	M0030	M0030_SAVINGS	SAVINGS	61612.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:08.806909	admin
337	M0002	M0002_SAVINGS	SAVINGS	53300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:54.549019	admin
338	M0003	M0003_SAVINGS	SAVINGS	38657.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:54.714154	admin
404	M0069	M0069_SAVINGS	SAVINGS	161239.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:18.753314	admin
554	M0219	M0219_SAVINGS	SAVINGS	1625.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:52.9762	admin
520	M0185	M0185_SAVINGS	SAVINGS	3735.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:41.90171	admin
510	M0175	M0175_SAVINGS	SAVINGS	15000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:39.11657	admin
601	M0267	M0267_SAVINGS	SAVINGS	22300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.524366	admin
537	M0202	M0202_SAVINGS	SAVINGS	8226.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:47.731618	admin
394	M0059	M0059_SAVINGS	SAVINGS	187042.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.989362	admin
341	M0006	M0006_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
370	M0035	M0035_SAVINGS	SAVINGS	90395.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:10.389428	admin
343	M0008	M0008_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
77	M000GL	M000GL_MM_INT	INCOME	0.00	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-18 22:16:49.738445	admin
361	M0026	M0026_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
78	M000GL	M000GL_EXPS	EXPENSE	0.00	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-18 22:16:49.738445	admin
364	M0029	M0029_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
369	M0034	M0034_SAVINGS	SAVINGS	35500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:09.444324	admin
385	M0050	M0050_SAVINGS	SAVINGS	21126.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:14.430724	admin
354	M0019	M0019_SAVINGS	SAVINGS	2969.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:00.417498	admin
367	M0032	M0032_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
372	M0037	M0037_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
373	M0038	M0038_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
374	M0039	M0039_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
357	M0022	M0022_SAVINGS	SAVINGS	101600.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:03.255211	admin
376	M0041	M0041_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
379	M0044	M0044_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
344	M0009	M0009_SAVINGS	SAVINGS	67405.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:56.229729	admin
382	M0047	M0047_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
383	M0048	M0048_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
355	M0020	M0020_SAVINGS	SAVINGS	152550.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:01.382425	admin
387	M0052	M0052_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
388	M0053	M0053_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
395	M0060	M0060_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
349	M0014	M0014_SAVINGS	SAVINGS	19500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:58.574289	admin
396	M0061	M0061_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
400	M0065	M0065_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
366	M0031	M0031_SAVINGS	SAVINGS	638.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:08.869747	admin
352	M0017	M0017_SAVINGS	SAVINGS	52000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:59.664849	admin
353	M0018	M0018_SAVINGS	SAVINGS	112040.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:00.315558	admin
438	M0103	M0103_SAVINGS	SAVINGS	16724.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.430453	admin
359	M0024	M0024_SAVINGS	SAVINGS	21333.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:04.786702	admin
368	M0033	M0033_SAVINGS	SAVINGS	1072.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:08.901068	admin
384	M0049	M0049_SAVINGS	SAVINGS	118750.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:14.314786	admin
477	M0142	M0142_SAVINGS	SAVINGS	1542.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.710187	admin
390	M0055	M0055_SAVINGS	SAVINGS	3752.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.297068	admin
492	M0157	M0157_SAVINGS	SAVINGS	13049.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:32.056609	admin
392	M0057	M0057_SAVINGS	SAVINGS	2144.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.423549	admin
386	M0051	M0051_SAVINGS	SAVINGS	322224.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.085666	admin
466	M0131	M0131_SAVINGS	SAVINGS	12404.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.257051	admin
426	M0091	M0091_SAVINGS	SAVINGS	11000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.690216	admin
479	M0144	M0144_SAVINGS	SAVINGS	2823.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.955702	admin
538	M0203	M0203_SAVINGS	SAVINGS	91000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:48.120392	admin
603	M0280	M0280_SAVINGS	SAVINGS	1000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.5843	admin
393	M0058	M0058_SAVINGS	SAVINGS	2321.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.474133	admin
570	M0235	M0235_SAVINGS	SAVINGS	147954.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.621813	admin
555	M0220	M0220_SAVINGS	SAVINGS	5051.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.096483	admin
552	M0217	M0217_SAVINGS	SAVINGS	10751.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:52.929662	admin
377	M0042	M0042_SAVINGS	SAVINGS	23000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:12.606658	admin
339	M0004	M0004_SAVINGS	SAVINGS	11598.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:54.86464	admin
345	M0010	M0010_SAVINGS	SAVINGS	67013.32	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-24 23:17:06.195145	admin
593	M0258	M0258_SAVINGS	SAVINGS	7727.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.049339	admin
407	M0072	M0072_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
391	M0056	M0056_SAVINGS	SAVINGS	4016.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.387279	admin
397	M0062	M0062_SAVINGS	SAVINGS	19283.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:16.084678	admin
403	M0068	M0068_SAVINGS	SAVINGS	74474.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:17.626633	admin
375	M0040	M0040_SAVINGS	SAVINGS	70346.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:12.512238	admin
408	M0073	M0073_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
413	M0078	M0078_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
418	M0083	M0083_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
419	M0084	M0084_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
422	M0087	M0087_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
423	M0088	M0088_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
424	M0089	M0089_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
425	M0090	M0090_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
428	M0093	M0093_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
429	M0094	M0094_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
435	M0100	M0100_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
441	M0106	M0106_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
448	M0113	M0113_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
451	M0116	M0116_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
455	M0120	M0120_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
340	M0005	M0005_SAVINGS	SAVINGS	12077.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:54.970467	admin
456	M0121	M0121_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
464	M0129	M0129_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
467	M0132	M0132_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
342	M0007	M0007_SAVINGS	SAVINGS	96397.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:55.485399	admin
346	M0011	M0011_SAVINGS	SAVINGS	165392.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:57.620158	admin
473	M0138	M0138_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
474	M0139	M0139_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
475	M0140	M0140_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
351	M0016	M0016_SAVINGS	SAVINGS	155965.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:59.634195	admin
493	M0158	M0158_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
495	M0160	M0160_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
496	M0161	M0161_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
498	M0163	M0163_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
347	M0012	M0012_SAVINGS	SAVINGS	235669.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:58.159736	admin
350	M0015	M0015_SAVINGS	SAVINGS	101488.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:59.04905	admin
399	M0064	M0064_SAVINGS	SAVINGS	7050.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:16.473702	admin
360	M0025	M0025_SAVINGS	SAVINGS	8000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:04.852001	admin
381	M0046	M0046_SAVINGS	SAVINGS	98500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:13.839452	admin
398	M0063	M0063_SAVINGS	SAVINGS	109979.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:16.397421	admin
405	M0070	M0070_SAVINGS	SAVINGS	161260.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:19.846536	admin
410	M0075	M0075_SAVINGS	SAVINGS	500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:19.981981	admin
412	M0077	M0077_SAVINGS	SAVINGS	1300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:20.942214	admin
409	M0074	M0074_SAVINGS	SAVINGS	2680.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:19.966821	admin
416	M0081	M0081_SAVINGS	SAVINGS	2144.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.35928	admin
411	M0076	M0076_SAVINGS	SAVINGS	361950.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:20.926977	admin
415	M0080	M0080_SAVINGS	SAVINGS	84622.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.329163	admin
580	M0245	M0245_SAVINGS	SAVINGS	3760.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.999996	admin
414	M0079	M0079_SAVINGS	SAVINGS	42864.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:21.983336	admin
420	M0085	M0085_SAVINGS	SAVINGS	500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.539522	admin
417	M0082	M0082_SAVINGS	SAVINGS	13000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.524713	admin
569	M0234	M0234_SAVINGS	SAVINGS	3182.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.200872	admin
549	M0214	M0214_SAVINGS	SAVINGS	29226.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:52.193398	admin
430	M0095	M0095_SAVINGS	SAVINGS	5730.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.895567	admin
607	M0284	M0284_SAVINGS	SAVINGS	700.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.748731	admin
581	M0246	M0246_SAVINGS	SAVINGS	186000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.183798	admin
356	M0021	M0021_SAVINGS	SAVINGS	92250.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:02.3931	admin
431	M0096	M0096_SAVINGS	SAVINGS	152852.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:24.617514	admin
427	M0092	M0092_SAVINGS	SAVINGS	2124.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.749677	admin
489	M0154	M0154_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
491	M0156	M0156_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
557	M0222	M0222_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
558	M0223	M0223_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
587	M0252	M0252_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
592	M0257	M0257_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
597	M0262	M0262_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
600	M0265	M0265_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
604	M0281	M0281_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
605	M0282	M0282_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
608	M0285	M0285_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
609	M0286	M0286_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
610	M0001	M0001_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
611	M0002	M0002_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
612	M0003	M0003_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
613	M0004	M0004_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
433	M0098	M0098_SAVINGS	SAVINGS	12692.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:24.903262	admin
432	M0097	M0097_SAVINGS	SAVINGS	167757.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:24.828898	admin
436	M0101	M0101_SAVINGS	SAVINGS	15044.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.008086	admin
434	M0099	M0099_SAVINGS	SAVINGS	638.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:24.962947	admin
439	M0104	M0104_SAVINGS	SAVINGS	1072.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.485726	admin
440	M0105	M0105_SAVINGS	SAVINGS	6947.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.651224	admin
445	M0110	M0110_SAVINGS	SAVINGS	4170.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:26.099943	admin
442	M0107	M0107_SAVINGS	SAVINGS	8447.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.794166	admin
443	M0108	M0108_SAVINGS	SAVINGS	638.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.868443	admin
444	M0109	M0109_SAVINGS	SAVINGS	2116.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.941371	admin
447	M0112	M0112_SAVINGS	SAVINGS	12000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:26.372661	admin
446	M0111	M0111_SAVINGS	SAVINGS	2291.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:26.208372	admin
453	M0118	M0118_SAVINGS	SAVINGS	5896.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:27.375696	admin
450	M0115	M0115_SAVINGS	SAVINGS	2291.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:26.553386	admin
454	M0119	M0119_SAVINGS	SAVINGS	51200.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:27.88868	admin
458	M0123	M0123_SAVINGS	SAVINGS	82679.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:28.477255	admin
457	M0122	M0122_SAVINGS	SAVINGS	26300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:27.981515	admin
459	M0124	M0124_SAVINGS	SAVINGS	3752.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:28.506905	admin
463	M0128	M0128_SAVINGS	SAVINGS	866.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.003145	admin
465	M0130	M0130_SAVINGS	SAVINGS	2000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.018192	admin
471	M0136	M0136_SAVINGS	SAVINGS	11432.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.541264	admin
468	M0133	M0133_SAVINGS	SAVINGS	718.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.316901	admin
469	M0134	M0134_SAVINGS	SAVINGS	1764.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.406929	admin
470	M0135	M0135_SAVINGS	SAVINGS	1260.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.466808	admin
472	M0137	M0137_SAVINGS	SAVINGS	2886.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.61908	admin
485	M0150	M0150_SAVINGS	SAVINGS	1608.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.50397	admin
480	M0145	M0145_SAVINGS	SAVINGS	32000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.276393	admin
483	M0148	M0148_SAVINGS	SAVINGS	1072.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.428041	admin
484	M0149	M0149_SAVINGS	SAVINGS	1072.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.458763	admin
487	M0152	M0152_SAVINGS	SAVINGS	16959.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.942926	admin
486	M0151	M0151_SAVINGS	SAVINGS	24800.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.653627	admin
488	M0153	M0153_SAVINGS	SAVINGS	3881.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:31.108001	admin
497	M0162	M0162_SAVINGS	SAVINGS	2665.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:32.466294	admin
490	M0155	M0155_SAVINGS	SAVINGS	62500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:31.941412	admin
501	M0166	M0166_SAVINGS	SAVINGS	250348.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:34.332389	admin
499	M0164	M0164_SAVINGS	SAVINGS	13800.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:32.526841	admin
512	M0177	M0177_SAVINGS	SAVINGS	1142.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:39.730922	admin
507	M0172	M0172_SAVINGS	SAVINGS	9221.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:37.733842	admin
509	M0174	M0174_SAVINGS	SAVINGS	39145.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:39.027414	admin
511	M0176	M0176_SAVINGS	SAVINGS	105693.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:39.685469	admin
515	M0180	M0180_SAVINGS	SAVINGS	186500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:40.603047	admin
513	M0178	M0178_SAVINGS	SAVINGS	1678.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:39.793706	admin
516	M0181	M0181_SAVINGS	SAVINGS	15910.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:40.948111	admin
544	M0209	M0209_SAVINGS	SAVINGS	44300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:51.680804	admin
539	M0204	M0204_SAVINGS	SAVINGS	261312.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:48.422721	admin
540	M0205	M0205_SAVINGS	SAVINGS	65312.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:48.643769	admin
460	M0125	M0125_SAVINGS	SAVINGS	37500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:36:19.209196	admin
503	M0168	M0168_SAVINGS	SAVINGS	169157.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:34.620123	admin
504	M0169	M0169_SAVINGS	SAVINGS	89500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:34.749687	admin
505	M0170	M0170_SAVINGS	SAVINGS	265543.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:35.026132	admin
553	M0218	M0218_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
517	M0182	M0182_SAVINGS	SAVINGS	91349.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:41.114496	admin
514	M0179	M0179_SAVINGS	SAVINGS	129868.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:40.097057	admin
619	M0010	M0010_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
620	M0011	M0011_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
621	M0012	M0012_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
622	M0013	M0013_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
623	M0014	M0014_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
624	M0015	M0015_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
625	M0016	M0016_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
519	M0184	M0184_SAVINGS	SAVINGS	41000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:41.658915	admin
626	M0017	M0017_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
627	M0018	M0018_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
628	M0019	M0019_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
629	M0020	M0020_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
630	M0021	M0021_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
631	M0022	M0022_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
632	M0023	M0023_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
633	M0024	M0024_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
634	M0025	M0025_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
635	M0026	M0026_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
636	M0027	M0027_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
637	M0028	M0028_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
638	M0029	M0029_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
639	M0030	M0030_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
640	M0031	M0031_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
641	M0032	M0032_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
642	M0033	M0033_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
643	M0034	M0034_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
644	M0035	M0035_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
526	M0191	M0191_SAVINGS	SAVINGS	36432.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:44.684095	admin
521	M0186	M0186_SAVINGS	SAVINGS	70784.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:42.913145	admin
522	M0187	M0187_SAVINGS	SAVINGS	22841.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:43.066398	admin
523	M0188	M0188_SAVINGS	SAVINGS	11332.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:43.216958	admin
525	M0190	M0190_SAVINGS	SAVINGS	247691.58	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-25 06:54:24.502287	admin
527	M0192	M0192_SAVINGS	SAVINGS	2144.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:44.728927	admin
528	M0193	M0193_SAVINGS	SAVINGS	55000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:44.803707	admin
530	M0195	M0195_SAVINGS	SAVINGS	5346.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:45.094998	admin
533	M0198	M0198_SAVINGS	SAVINGS	334.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:46.898808	admin
531	M0196	M0196_SAVINGS	SAVINGS	3500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:45.421174	admin
536	M0201	M0201_SAVINGS	SAVINGS	250771.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:47.551063	admin
534	M0199	M0199_SAVINGS	SAVINGS	536.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:46.960115	admin
535	M0200	M0200_SAVINGS	SAVINGS	4185.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:47.141648	admin
542	M0207	M0207_SAVINGS	SAVINGS	2494.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:49.110817	admin
541	M0206	M0206_SAVINGS	SAVINGS	91312.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:48.764226	admin
550	M0215	M0215_SAVINGS	SAVINGS	2775.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:52.29826	admin
543	M0208	M0208_SAVINGS	SAVINGS	95400.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:51.33349	admin
546	M0211	M0211_SAVINGS	SAVINGS	28500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:51.830836	admin
547	M0212	M0212_SAVINGS	SAVINGS	5739.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:51.982157	admin
548	M0213	M0213_SAVINGS	SAVINGS	1972.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:52.042407	admin
565	M0230	M0230_SAVINGS	SAVINGS	6415.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.005696	admin
560	M0225	M0225_SAVINGS	SAVINGS	25000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.598231	admin
566	M0231	M0231_SAVINGS	SAVINGS	109650.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.1108	admin
567	M0232	M0232_SAVINGS	SAVINGS	30.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.125742	admin
571	M0236	M0236_SAVINGS	SAVINGS	1052.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.666549	admin
596	M0261	M0261_SAVINGS	SAVINGS	500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.208495	admin
582	M0247	M0247_SAVINGS	SAVINGS	6300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.274097	admin
583	M0248	M0248_SAVINGS	SAVINGS	1102.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.335483	admin
584	M0249	M0249_SAVINGS	SAVINGS	9204.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.504477	admin
585	M0250	M0250_SAVINGS	SAVINGS	10589.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.660473	admin
586	M0251	M0251_SAVINGS	SAVINGS	1000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.697233	admin
589	M0254	M0254_SAVINGS	SAVINGS	308.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.77661	admin
590	M0255	M0255_SAVINGS	SAVINGS	15590.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.885312	admin
591	M0256	M0256_SAVINGS	SAVINGS	308.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.923376	admin
645	M0036	M0036_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
646	M0037	M0037_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
647	M0038	M0038_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
648	M0039	M0039_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
649	M0040	M0040_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
650	M0041	M0041_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
651	M0042	M0042_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
652	M0043	M0043_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
653	M0044	M0044_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
654	M0045	M0045_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
655	M0046	M0046_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
656	M0047	M0047_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
657	M0048	M0048_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
658	M0049	M0049_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
659	M0050	M0050_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
660	M0051	M0051_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
661	M0052	M0052_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
662	M0053	M0053_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
663	M0054	M0054_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
664	M0055	M0055_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
665	M0056	M0056_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
666	M0057	M0057_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
667	M0058	M0058_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
668	M0059	M0059_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
669	M0060	M0060_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
670	M0061	M0061_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
671	M0062	M0062_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
672	M0063	M0063_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
673	M0064	M0064_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
674	M0065	M0065_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
675	M0066	M0066_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
676	M0067	M0067_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
677	M0068	M0068_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
678	M0069	M0069_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
679	M0070	M0070_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
680	M0071	M0071_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
681	M0072	M0072_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
682	M0073	M0073_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
683	M0074	M0074_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
684	M0075	M0075_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
685	M0076	M0076_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
686	M0077	M0077_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
687	M0078	M0078_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
688	M0079	M0079_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
689	M0080	M0080_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
690	M0081	M0081_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
691	M0082	M0082_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
692	M0083	M0083_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
693	M0084	M0084_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
694	M0085	M0085_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
695	M0086	M0086_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
696	M0087	M0087_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
559	M0224	M0224_SAVINGS	SAVINGS	25571.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.324458	admin
561	M0226	M0226_SAVINGS	SAVINGS	8884.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.67379	admin
562	M0227	M0227_SAVINGS	SAVINGS	2430.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.720409	admin
573	M0238	M0238_SAVINGS	SAVINGS	5623.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.021156	admin
563	M0228	M0228_SAVINGS	SAVINGS	2824.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.780475	admin
564	M0229	M0229_SAVINGS	SAVINGS	37300.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.870032	admin
572	M0237	M0237_SAVINGS	SAVINGS	13873.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.885541	admin
576	M0241	M0241_SAVINGS	SAVINGS	11568.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.155931	admin
574	M0239	M0239_SAVINGS	SAVINGS	522.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.050801	admin
575	M0240	M0240_SAVINGS	SAVINGS	1899.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.081085	admin
594	M0259	M0259_SAVINGS	SAVINGS	1413.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.132095	admin
599	M0264	M0264_SAVINGS	SAVINGS	64804.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.404865	admin
595	M0260	M0260_SAVINGS	SAVINGS	511.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.162632	admin
598	M0263	M0263_SAVINGS	SAVINGS	303325.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.238478	admin
602	M0268	M0268_SAVINGS	SAVINGS	500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.539602	admin
606	M0283	M0283_SAVINGS	SAVINGS	3500.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:32:00.644208	admin
697	M0088	M0088_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
698	M0089	M0089_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
699	M0090	M0090_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
700	M0091	M0091_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
701	M0092	M0092_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
702	M0093	M0093_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
703	M0094	M0094_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
704	M0095	M0095_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
705	M0096	M0096_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
706	M0097	M0097_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
707	M0098	M0098_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
708	M0099	M0099_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
709	M0100	M0100_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
710	M0101	M0101_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
711	M0102	M0102_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
712	M0103	M0103_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
713	M0104	M0104_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
714	M0105	M0105_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
715	M0106	M0106_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
716	M0107	M0107_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
717	M0108	M0108_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
718	M0109	M0109_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
719	M0110	M0110_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
720	M0111	M0111_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
721	M0112	M0112_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
722	M0113	M0113_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
723	M0114	M0114_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
724	M0115	M0115_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
725	M0116	M0116_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
726	M0117	M0117_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
727	M0118	M0118_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
728	M0119	M0119_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
729	M0120	M0120_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
730	M0121	M0121_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
731	M0122	M0122_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
732	M0123	M0123_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
733	M0124	M0124_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
734	M0125	M0125_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
506	M0171	M0171_SAVINGS	SAVINGS	244840.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:37.661924	admin
735	M0126	M0126_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
736	M0127	M0127_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
737	M0128	M0128_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
738	M0129	M0129_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
739	M0130	M0130_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
740	M0131	M0131_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
741	M0132	M0132_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
742	M0133	M0133_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
743	M0134	M0134_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
744	M0135	M0135_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
745	M0136	M0136_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
746	M0137	M0137_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
747	M0138	M0138_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
748	M0139	M0139_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
749	M0140	M0140_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
750	M0141	M0141_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
751	M0142	M0142_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
752	M0143	M0143_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
753	M0144	M0144_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
754	M0145	M0145_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
755	M0146	M0146_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
756	M0147	M0147_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
757	M0148	M0148_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
758	M0149	M0149_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
759	M0150	M0150_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
760	M0151	M0151_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
761	M0152	M0152_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
762	M0153	M0153_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
763	M0154	M0154_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
764	M0155	M0155_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
765	M0156	M0156_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
766	M0157	M0157_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
767	M0158	M0158_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
768	M0159	M0159_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
769	M0160	M0160_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
770	M0161	M0161_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
771	M0162	M0162_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
772	M0163	M0163_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
773	M0164	M0164_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
774	M0165	M0165_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
775	M0166	M0166_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
776	M0167	M0167_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
777	M0168	M0168_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
778	M0169	M0169_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
779	M0170	M0170_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
780	M0171	M0171_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
781	M0172	M0172_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
782	M0173	M0173_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
783	M0174	M0174_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
784	M0175	M0175_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
578	M0243	M0243_SAVINGS	SAVINGS	3363.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.744014	admin
785	M0176	M0176_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
786	M0177	M0177_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
787	M0178	M0178_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
788	M0179	M0179_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
789	M0180	M0180_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
790	M0181	M0181_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
791	M0182	M0182_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
792	M0183	M0183_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
793	M0184	M0184_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
794	M0185	M0185_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
795	M0186	M0186_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
796	M0187	M0187_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
797	M0188	M0188_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
798	M0189	M0189_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
799	M0190	M0190_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
800	M0191	M0191_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
801	M0192	M0192_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
802	M0193	M0193_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
803	M0194	M0194_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
804	M0195	M0195_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
805	M0196	M0196_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
806	M0197	M0197_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
807	M0198	M0198_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
808	M0199	M0199_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
809	M0200	M0200_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
810	M0201	M0201_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
811	M0202	M0202_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
812	M0203	M0203_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
813	M0204	M0204_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
814	M0205	M0205_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
815	M0206	M0206_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
816	M0207	M0207_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
817	M0208	M0208_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
818	M0209	M0209_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
819	M0210	M0210_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
820	M0211	M0211_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
821	M0212	M0212_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
822	M0213	M0213_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
823	M0214	M0214_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
824	M0215	M0215_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
825	M0216	M0216_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
826	M0217	M0217_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
827	M0218	M0218_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
828	M0219	M0219_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
829	M0220	M0220_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
830	M0221	M0221_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
831	M0222	M0222_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
832	M0223	M0223_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
835	M0226	M0226_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
836	M0227	M0227_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
833	M0224	M0224_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
834	M0225	M0225_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
837	M0228	M0228_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
838	M0229	M0229_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
839	M0230	M0230_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
840	M0231	M0231_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
841	M0232	M0232_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
401	M0066	M0066_SAVINGS	SAVINGS	4288.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:16.567988	admin
842	M0233	M0233_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
843	M0234	M0234_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
844	M0235	M0235_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
845	M0236	M0236_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
846	M0237	M0237_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
847	M0238	M0238_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
848	M0239	M0239_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
849	M0240	M0240_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
850	M0241	M0241_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
851	M0242	M0242_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
852	M0243	M0243_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
853	M0244	M0244_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
854	M0245	M0245_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
855	M0246	M0246_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
856	M0247	M0247_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
877	M0280	M0280_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
878	M0281	M0281_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
879	M0282	M0282_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
880	M0283	M0283_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
881	M0284	M0284_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
882	M0285	M0285_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
883	M0286	M0286_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
449	M0114	M0114_SAVINGS	SAVINGS	7611.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:26.493265	admin
551	M0216	M0216_SAVINGS	SAVINGS	6498.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:52.390051	admin
437	M0102	M0102_SAVINGS	SAVINGS	901.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:25.052253	admin
371	M0036	M0036_SAVINGS	SAVINGS	74000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:11.480415	admin
389	M0054	M0054_SAVINGS	SAVINGS	11820.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:15.236515	admin
348	M0013	M0013_SAVINGS	SAVINGS	22786.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:30:58.223014	admin
462	M0127	M0127_SAVINGS	SAVINGS	3752.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:28.958442	admin
406	M0071	M0071_SAVINGS	SAVINGS	4246.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:19.936773	admin
358	M0023	M0023_SAVINGS	SAVINGS	65959.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:04.29314	admin
556	M0221	M0221_SAVINGS	SAVINGS	1909.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:53.126813	admin
476	M0141	M0141_SAVINGS	SAVINGS	306.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.649812	admin
494	M0159	M0159_SAVINGS	SAVINGS	25000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:32.390464	admin
518	M0183	M0183_SAVINGS	SAVINGS	131000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:41.583916	admin
421	M0086	M0086_SAVINGS	SAVINGS	7000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:23.58428	admin
529	M0194	M0194_SAVINGS	SAVINGS	219208.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:44.966832	admin
579	M0244	M0244_SAVINGS	SAVINGS	110000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.910016	admin
481	M0146	M0146_SAVINGS	SAVINGS	3337.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.323442	admin
336	M0001	M0001_SAVINGS	SAVINGS	57991.13	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-24 21:51:56.937802	admin
568	M0233	M0233_SAVINGS	SAVINGS	451.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:54.170874	admin
588	M0253	M0253_SAVINGS	SAVINGS	309.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:59.739236	admin
508	M0173	M0173_SAVINGS	SAVINGS	44252.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:38.295924	admin
577	M0242	M0242_SAVINGS	SAVINGS	8394.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:55.427054	admin
71	M000GL	M000GL_LOAN	LOANS	86173.36	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-25 07:28:53.939807	admin
76	M000GL	M000GL_REG_FEE	INCOME	1250.00	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-25 07:28:53.939812	admin
363	M0028	M0028_SAVINGS	SAVINGS	2303.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:08.311809	admin
380	M0045	M0045_SAVINGS	SAVINGS	9600.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:13.603004	admin
378	M0043	M0043_SAVINGS	SAVINGS	73402.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:13.215876	admin
72	M000GL	M000GL_SAVINGS	SAVINGS	10305949.61	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-25 06:54:24.502273	admin
74	M000GL	M000GL_LN_INT	INCOME	8494.33	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-25 06:54:24.50228	admin
73	M000GL	M000GL_SHARE_CAP	EQUITY	0.00	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-18 22:16:49.738445	admin
75	M000GL	M000GL_LN_APP_FEE	INCOME	0.00	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-18 22:16:49.738445	admin
402	M0067	M0067_SAVINGS	SAVINGS	21000.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:16.615034	admin
461	M0126	M0126_SAVINGS	SAVINGS	92919.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-24 21:04:17.23369	admin
912	M0009	M0010_LOAN	LOAN	134500.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
913	M0010	M0011_LOAN	LOAN	170135.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
914	M0011	M0022_LOAN	LOAN	179668.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
915	M0022	M0023_LOAN	LOAN	108168.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
916	M0023	M0027_LOAN	LOAN	180000.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
917	M0027	M0051_LOAN	LOAN	382082.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
918	M0051	M0054_LOAN	LOAN	761724.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
919	M0054	M0059_LOAN	LOAN	21362.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
920	M0059	M0063_LOAN	LOAN	620000.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
921	M0063	M0076_LOAN	LOAN	125245.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
922	M0076	M0079_LOAN	LOAN	795871.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
923	M0079	M0123_LOAN	LOAN	58540.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
924	M0123	M0131_LOAN	LOAN	158664.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
925	M0131	M0163_LOAN	LOAN	17964.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
926	M0163	M0166_LOAN	LOAN	10118.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
927	M0166	M0168_LOAN	LOAN	677801.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
928	M0168	M0171_LOAN	LOAN	228356.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
929	M0171	M0174_LOAN	LOAN	581341.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
930	M0174	M0179_LOAN	LOAN	13917.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
931	M0179	M0180_LOAN	LOAN	350000.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
932	M0180	M0182_LOAN	LOAN	406505.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
933	M0182	M0186_LOAN	LOAN	183250.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
934	M0186	M0195_LOAN	LOAN	95436.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
935	M0195	M0197_LOAN	LOAN	7212.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
936	M0197	M0203_LOAN	LOAN	75404.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
937	M0203	M0204_LOAN	LOAN	300000.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
938	M0204	M0206_LOAN	LOAN	226625.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
939	M0206	M0208_LOAN	LOAN	350000.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
940	M0208	M0224_LOAN	LOAN	161671.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
941	M0224	M0244_LOAN	LOAN	120000.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
942	M0244	M0246_LOAN	LOAN	203234.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
943	M0246	M0009_LOAN	LOAN	358047.00	2000000.00	active	2025-10-25 11:00:56.954239	2025-10-25 11:00:56.954239	admin
946	M0009	M0009_INTEREST	INTEREST	1681.25	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
947	M0010	M0010_INTEREST	INTEREST	2126.69	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
948	M0011	M0011_INTEREST	INTEREST	2245.85	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
949	M0022	M0022_INTEREST	INTEREST	1352.10	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
950	M0023	M0023_INTEREST	INTEREST	2250.00	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
951	M0027	M0027_INTEREST	INTEREST	4776.03	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
952	M0051	M0051_INTEREST	INTEREST	9521.55	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
953	M0054	M0054_INTEREST	INTEREST	267.03	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
954	M0059	M0059_INTEREST	INTEREST	7750.00	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
955	M0063	M0063_INTEREST	INTEREST	1565.56	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
956	M0076	M0076_INTEREST	INTEREST	9948.39	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
957	M0079	M0079_INTEREST	INTEREST	731.75	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
958	M0123	M0123_INTEREST	INTEREST	1983.30	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
959	M0131	M0131_INTEREST	INTEREST	224.55	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
960	M0163	M0163_INTEREST	INTEREST	126.48	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
961	M0166	M0166_INTEREST	INTEREST	8472.51	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
962	M0168	M0168_INTEREST	INTEREST	2854.45	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
963	M0171	M0171_INTEREST	INTEREST	7266.76	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
964	M0174	M0174_INTEREST	INTEREST	173.96	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
965	M0179	M0179_INTEREST	INTEREST	4375.00	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
966	M0180	M0180_INTEREST	INTEREST	5081.31	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
967	M0182	M0182_INTEREST	INTEREST	2290.62	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
968	M0186	M0186_INTEREST	INTEREST	1192.95	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
969	M0195	M0195_INTEREST	INTEREST	90.15	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
970	M0197	M0197_INTEREST	INTEREST	942.55	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
971	M0203	M0203_INTEREST	INTEREST	3750.00	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
972	M0204	M0204_INTEREST	INTEREST	2832.81	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
973	M0206	M0206_INTEREST	INTEREST	4375.00	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
478	M0143	M0143_SAVINGS	SAVINGS	22123.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:29.909304	admin
482	M0147	M0147_SAVINGS	SAVINGS	255697.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-19 18:31:30.397826	admin
974	M0208	M0208_INTEREST	INTEREST	2020.88	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
975	M0224	M0224_INTEREST	INTEREST	1500.00	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
976	M0244	M0244_INTEREST	INTEREST	2540.42	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
977	M0246	M0246_INTEREST	INTEREST	4475.58	2000000.00	active	2025-10-25 11:21:42.648565	2025-10-25 11:21:42.648565	admin
500	M0165	M0165_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
502	M0167	M0167_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
524	M0189	M0189_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
545	M0210	M0210_SAVINGS	SAVINGS	0.00	2000000.00	active	2025-10-18 22:58:20.065576	2025-10-18 22:58:20.065576	admin
614	M0005	M0005_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
615	M0006	M0006_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
616	M0007	M0007_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
617	M0008	M0008_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
618	M0009	M0009_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
70	M000GL	M000GL_CASH	CASH_ACC	10104112.00	100000000.00	active	2025-10-18 22:16:49.738445	2025-10-25 07:28:53.939798	admin
857	M0248	M0248_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
858	M0249	M0249_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
859	M0250	M0250_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
860	M0251	M0251_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
861	M0252	M0252_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
862	M0253	M0253_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
863	M0254	M0254_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
864	M0255	M0255_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
865	M0256	M0256_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
866	M0257	M0257_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
867	M0258	M0258_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
868	M0259	M0259_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
869	M0260	M0260_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
870	M0261	M0261_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
871	M0262	M0262_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
872	M0263	M0263_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
873	M0264	M0264_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
874	M0265	M0265_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
875	M0267	M0267_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
876	M0268	M0268_SHARE_CAP	SHARE_CAPITAL	0.00	2000000.00	active	2025-10-18 23:05:25.212921	2025-10-18 23:05:25.212921	admin
\.


--
-- Data for Name: savings_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.savings_accounts (id, member_id, balance) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transactions (id, created_at, txn_no, member_no, account_no, gl_account, running_balance, reference, narration, bank_txn_date, tran_type, posted_by, debit_amount, credit_amount) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, role, member_id, created_at) FROM stdin;
1	admin	admin@sacco.local	scrypt:32768:8:1$5ITRP79lSWvDA99e$7c0774fd7f1016a64f2a94c8b9d6accd4448693cfa1646de63c8b82120eb55b5ce39d5e741ccb13202e40afb826eb1d45bea56a7095007f2b1e7deb74c504b76	admin	\N	2025-10-10 08:14:08.64024
2	jkariokoo	kariokojim@gmail.com	scrypt:32768:8:1$oBsVsaHhbXhU6uoA$a6bbca79e6bd63c40991b140fcf809ead871a142380c5c8275ec33d39731aac031919ec32b690d2c8345432fd6da126eaf923b5141ab41c9d58390ee31de95ba	admin	\N	2025-10-10 21:03:10.581689
3	agitau	agmuiruri@gmail.com	scrypt:32768:8:1$PpDGiSyw1LMd4mIr$7b704b796d37e3e820ed8f3b2f1358522e902841fe2feb57f07372e315e784a0cfdcb2477f256a43578123aa69bfe300652af1072aec4af0ed3c61e714772b82	staff	\N	2025-10-10 21:20:37.59705
4	rgitau	akmuiruri@gmail.com	scrypt:32768:8:1$ROsB7uhEFCd5qkHV$b748a9ee956180ec43500a506d097ff17449b6741f2ffb374074080a9ec77e0c528a2849823907a6d26a66c46a91109ae659ce94f4d7253cefb1af8a2563a686	staff	\N	2025-10-11 11:52:07.685218
\.


--
-- Name: gl_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gl_accounts_id_seq', 2, true);


--
-- Name: gl_postings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gl_postings_id_seq', 1, false);


--
-- Name: gl_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gl_transactions_id_seq', 34, true);


--
-- Name: loan_guarantors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loan_guarantors_id_seq', 18, true);


--
-- Name: loan_interest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loan_interest_id_seq', 9, true);


--
-- Name: loan_schedules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loan_schedules_id_seq', 1289, true);


--
-- Name: loans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loans_id_seq', 61, true);


--
-- Name: members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.members_id_seq', 568, true);


--
-- Name: sacco_accounts_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sacco_accounts_account_id_seq', 977, true);


--
-- Name: savings_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.savings_accounts_id_seq', 1, false);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transactions_id_seq', 89660, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: gl_accounts gl_accounts_gl_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_accounts
    ADD CONSTRAINT gl_accounts_gl_code_key UNIQUE (gl_code);


--
-- Name: gl_accounts gl_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_accounts
    ADD CONSTRAINT gl_accounts_pkey PRIMARY KEY (id);


--
-- Name: gl_postings gl_postings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_postings
    ADD CONSTRAINT gl_postings_pkey PRIMARY KEY (id);


--
-- Name: gl_transactions gl_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_transactions
    ADD CONSTRAINT gl_transactions_pkey PRIMARY KEY (id);


--
-- Name: loan_guarantors loan_guarantors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_guarantors
    ADD CONSTRAINT loan_guarantors_pkey PRIMARY KEY (id);


--
-- Name: loan_interest loan_interest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_interest
    ADD CONSTRAINT loan_interest_pkey PRIMARY KEY (id);


--
-- Name: loan_schedules loan_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_schedules
    ADD CONSTRAINT loan_schedules_pkey PRIMARY KEY (id);


--
-- Name: loans loans_loan_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_loan_no_key UNIQUE (loan_no);


--
-- Name: loans loans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_pkey PRIMARY KEY (id);


--
-- Name: members members_member_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_member_no_key UNIQUE (member_no);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- Name: sacco_accounts sacco_accounts_account_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sacco_accounts
    ADD CONSTRAINT sacco_accounts_account_number_key UNIQUE (account_number);


--
-- Name: sacco_accounts sacco_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sacco_accounts
    ADD CONSTRAINT sacco_accounts_pkey PRIMARY KEY (account_id);


--
-- Name: savings_accounts savings_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings_accounts
    ADD CONSTRAINT savings_accounts_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_txn_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_txn_no_key UNIQUE (txn_no);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: gl_transactions gl_transactions_gl_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gl_transactions
    ADD CONSTRAINT gl_transactions_gl_code_fkey FOREIGN KEY (gl_code) REFERENCES public.gl_accounts(gl_code);


--
-- Name: loan_guarantors loan_guarantors_loan_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_guarantors
    ADD CONSTRAINT loan_guarantors_loan_no_fkey FOREIGN KEY (loan_no) REFERENCES public.loans(loan_no);


--
-- Name: loan_guarantors loan_guarantors_member_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_guarantors
    ADD CONSTRAINT loan_guarantors_member_no_fkey FOREIGN KEY (member_no) REFERENCES public.members(member_no);


--
-- Name: loan_interest loan_interest_loan_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_interest
    ADD CONSTRAINT loan_interest_loan_no_fkey FOREIGN KEY (loan_no) REFERENCES public.loans(loan_no);


--
-- Name: loan_schedules loan_schedules_loan_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_schedules
    ADD CONSTRAINT loan_schedules_loan_no_fkey FOREIGN KEY (loan_no) REFERENCES public.loans(loan_no);


--
-- Name: loan_schedules loan_schedules_member_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loan_schedules
    ADD CONSTRAINT loan_schedules_member_no_fkey FOREIGN KEY (member_no) REFERENCES public.members(member_no);


--
-- Name: loans loans_disbursed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_disbursed_by_fkey FOREIGN KEY (disbursed_by) REFERENCES public.users(id);


--
-- Name: loans loans_member_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_member_no_fkey FOREIGN KEY (member_no) REFERENCES public.members(member_no);


--
-- Name: members members_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: sacco_accounts sacco_accounts_member_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sacco_accounts
    ADD CONSTRAINT sacco_accounts_member_no_fkey FOREIGN KEY (member_no) REFERENCES public.members(member_no);


--
-- Name: savings_accounts savings_accounts_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.savings_accounts
    ADD CONSTRAINT savings_accounts_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- Name: transactions transactions_account_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_account_no_fkey FOREIGN KEY (account_no) REFERENCES public.sacco_accounts(account_number);


--
-- Name: transactions transactions_member_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_member_no_fkey FOREIGN KEY (member_no) REFERENCES public.members(member_no);


--
-- Name: users users_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

