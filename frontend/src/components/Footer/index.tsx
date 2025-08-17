function Footer() {
    return (
        <footer className="bg-white border-t mt-auto">
            <div className="container mx-auto px-4 py-6">
                <div className="flex flex-col md:flex-row items-center justify-between">
                    <div className="flex items-center space-x-4 mb-4 md:mb-0">
                        <div className="w-6 h-6 bg-blue-500 rounded flex items-center justify-center">
                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-1l-4 4z" />
                            </svg>
                        </div>
                        <span className="text-gray-600">© 2024 ChatPDF. All rights reserved.</span>
                    </div>
                    <div className="flex items-center space-x-6 text-sm text-gray-500">
                        <span>Built with React & Flask</span>
                    </div>
                </div>
            </div>
        </footer>
    )
}
export default Footer;